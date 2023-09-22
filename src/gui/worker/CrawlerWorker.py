from PyQt5.QtCore import QObject, pyqtSignal


import json
import os
import subprocess
import time
import sys

sys.path.append(os.path.join(os.getcwd()))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from src.utils.PrintUtils import print_log
from src.utils.SeleniumUtils import UserActivity
from src.utils.DayCompleteUtils import whether_day_has_reservation_before, get_day_complete_string


class CrawlerWorker(QObject):
    finished = pyqtSignal()
    start_check = pyqtSignal()
    logger = pyqtSignal(str, str)
    start_booking = pyqtSignal(str, str)

    def __init__(self, headless: bool, credential_mode, parent=None):
        super(CrawlerWorker, self).__init__(parent)
        self.message = ''
        self.headless = headless
        self.credential_mode = credential_mode
        self._is_running = True

    def __quit_driver(self, driver):
        try:
            driver.quit()
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')

    def wait_for_page_done_load(self, driver):
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.teetimeitem.ng-star-inserted')))

    def move_to_day(self, driver, css_selector):
        try:
            self.wait_for_page_done_load(driver)
            date_button = WebDriverWait(driver, 20).until(
                lambda x: x.find_element(By.CSS_SELECTOR, css_selector))
            date_button.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'rightlist')))
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

    def check_available_teetime(self, driver):
        try:
            no_teetime = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'divNoTeeTime')))
            return False
        except Exception as e:
            return True

    def check_for_each_day(self, driver, date):
        if self.credential_mode == 'signin':
            # Get the current email
            with open(os.path.join(os.getcwd(), 'data', 'sign_in.json'), 'r', encoding='utf8') as f:
                user_data = json.load(f)
                email = user_data['email']

            if whether_day_has_reservation_before(int(date), email):
                print_log(f'Date {get_day_complete_string(int(date))} has reservation before with email {email}, skip ...')
                self.logger.emit(
                    f'Date {get_day_complete_string(int(date))} has reservation before with email {email}, skip ...', 'blue')
                return False

        if self.check_available_teetime(driver):
            # Try to click the first available session on this date
            time.sleep(1)
            try:
                button = driver.execute_script("""
                        var buttons = document.querySelector("button.btnStepper");
                        return buttons.innerText;
                                               """)
            except Exception as e:
                print_log(f'Cannot click the first available session with error: {e}')
                self.logger.emit(f'Cannot click the first available session with error: {e}', 'red')
                return False

            session_info = button.split('\n')
            session_info.extend(session_info[1].split(' | '))
            del session_info[1]
            print_log(f'Found available tee time on date {date}: {session_info}')
            self.logger.emit(f'Found available tee time on date {date}: {session_info}', 'green')
            self.message += f'Found available tee time on date {date}: {session_info}\n\n'
            return True

        else:
            print_log(f'No available tee time on date {date}')
            self.logger.emit(f'No available tee time on date {date}', 'black')
            return False

    def process(self, booking_url):
        if self._is_running is False:
            return

        while True:
            browser = UserActivity(headless=self.headless)
            driver = browser.driver
            driver.implicitly_wait(10)
            current_active_dates = []

            # Open the booking page
            try:
                print_log(f'Opening booking page: {booking_url}')
                self.logger.emit(f'Opening booking page: {booking_url}', 'black')
                driver.get(booking_url)
                break
            except Exception as e:
                print_log(str(e))
                self.logger.emit(str(e))
                continue

        # Choose Riverway options
        if self._is_running is False:
            return
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'courses-selection')))
            time.sleep(1)
            print_log('Choosing Riverway option ...')
            self.logger.emit('Choosing Riverway option ...', 'black')
            with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'Riverway.js'), 'r', encoding='utf8') as f:
                js = f.read()
            driver.execute_script(js)
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Choose the 4 player button
        if self._is_running is False:
            return
        try:
            time.sleep(1)
            print_log('Choosing 4 players option ...')
            self.logger.emit('Choosing 4 players option ...', 'black')
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, 'mat-button-toggle-4-button')))
            driver.execute_script("""
                var button = document.getElementById('mat-button-toggle-4-button');
                button.click();
                """)
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Get the current active date from execute script
        if self._is_running is False:
            return
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'main-calendar-container')))
            time.sleep(1)
            with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'GetActiveDate.js'), 'r', encoding='utf8') as f:
                js = f.read()
            current_active_dates = driver.execute_script(js)

            dates = [date for _, date in current_active_dates]

            print_log(f'Current active dates: {", ".join(dates)}')
            self.logger.emit(f'Current active dates: {", ".join(dates)}', 'black')
            self.message += f'Current active dates: {", ".join(dates)}\n\n'

        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        time.sleep(1)

        # Iterate through the dates, check whether exist any session available
        for css_selector, date in current_active_dates:
            if self._is_running is False:
                return
            else:
                print_log(f'Checking date: {date}')
                self.logger.emit(f'Checking date: {date}', 'black')
                self.move_to_day(driver, css_selector)
                check_result = self.check_for_each_day(driver, date)
                if check_result:
                    self.destroy()
                    self.__quit_driver(driver)
                    time.sleep(1)
                    self.start_booking.emit(css_selector, date)
                    return
                else:
                    continue

        self.__quit_driver(driver)

    def run(self):
        """
        CrawlerWorker's main method
        """
        # Load configuration
        config_path = os.path.join(os.getcwd(), 'configuration', 'crawler.json')
        with open(config_path, 'r', encoding='utf8') as f:
            config = json.load(f)
            check_period = config['check_period']  # In minutes
            start_time = config['start_time']  # In 24h format
            end_time = config['end_time']  # In 24h format
        # Constant URL
        booking_url = f"https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin={start_time}&TeeOffTimeMax={end_time}"

        # Run the crawler in a loop with a period of 5 minutes
        while self._is_running:
            print('-' * 120)
            self.start_check.emit()
            print_log(f'Start checking with time frame: {start_time}h - {end_time}h  - Riverway - 4 players')
            self.logger.emit(
                f'Start checking with time frame: {start_time}h - {end_time}h  - Riverway - 4 players', 'black')

            # Text to telegram
            self.message = ''
            self.message += f'Start checking with time frame: {start_time}h - {end_time}h - Riverway - 4 players\n\n'

            self.process(booking_url)

            if self._is_running:
                time.sleep(check_period * 60)
            else:
                print_log('Crawler stopped')
                self.logger.emit('Crawler stopped', 'green')

    def destroy(self):
        self._is_running = False
        self.logger.emit('Stopping crawler ...', 'red')
        print_log('Stopping crawler ...')
        self.finished.emit()
