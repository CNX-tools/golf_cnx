from PyQt5.QtCore import QObject, pyqtSignal


import json
import os
import subprocess
import time
import sys

# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(os.path.join(os.getcwd(), 'src'))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.TelegramBot import send_message
from utils.PrintUtils import print_log
from utils.SeleniumUtils import UserActivity


class CrawlerWorker(QObject):
    finished = pyqtSignal()
    start_check = pyqtSignal()
    logger = pyqtSignal(str, str)
    start_booking = pyqtSignal(str, str)

    def __init__(self, logs_output, headless: bool, parent=None):
        super(CrawlerWorker, self).__init__(parent)
        self.logs_output = logs_output
        self.message = ''
        self.headless = headless
        self._is_running = True

    def __quit_driver(self, driver):
        driver.quit()
        try:
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.finished.emit()

    def move_to_day(self, driver, css_selector):
        try:
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
            no_teetime = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CLASS_NAME, 'divNoTeeTime'))
            return False
        except Exception as e:
            return True

    def check_for_each_day(self, driver, date):
        if self.check_available_teetime(driver):
            # Try to click the first available session on this date
            try:
                button = WebDriverWait(driver, 30).until(
                    lambda x: x.find_element(By.CLASS_NAME, 'btnStepper'))
                session_info = button.text.split('\n')
                session_info.extend(session_info[1].split(' | '))
                del session_info[1]
                print_log(f'Found available tee time on date {date}: {session_info}')
                self.logger.emit(f'Found available tee time on date {date}: {session_info}', 'green')
                self.message += f'Found available tee time on date {date}: {session_info}\n\n'
                return True
            except Exception as e:
                print_log(f'Cannot click the first available session with error: {e}')
                self.logger.emit(f'Cannot click the first available session with error: {e}', 'red')
                return False
        else:
            print_log(f'No available tee time on date {date}')
            self.logger.emit(f'No available tee time on date {date}', 'black')
            return False

    def process(self, booking_url):
        browser = UserActivity(headless=self.headless)
        driver = browser.driver
        current_active_dates = []

        # Open the booking page
        if self._is_running is False:
            return False
        try:
            print_log(f'Opening booking page: {booking_url}')
            self.logger.emit(f'Opening booking page: {booking_url}', 'black')
            driver.get(booking_url)
        except Exception as e:
            print_log('Timeout, trying again ...')
            self.logger.emit('Timeout, trying again ...', 'black')
            driver.refresh()

        # Choose Riverway options
        if self._is_running is False:
            return False
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
            return False
        try:
            time.sleep(1)
            print_log('Choosing 4 players option ...')
            self.logger.emit('Choosing 4 players option ...', 'black')
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'mat-button-toggle-4-button'))
            )
            four_player_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.ID, 'mat-button-toggle-4-button'))
            four_player_button.click()
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Get the current active date from execute script
        if self._is_running is False:
            return False
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

        available_teetime = False
        # Iterate through the dates, check whether exist any session available
        for css_selector, date in current_active_dates:
            if self._is_running is False:
                return False
            else:
                print_log(f'Checking date: {date}')
                self.logger.emit(f'Checking date: {date}', 'black')
                self.move_to_day(driver, css_selector)
                time.sleep(2)
                check_result = self.check_for_each_day(driver, date)
                if check_result:
                    available_teetime = True
                    self.start_booking.emit(css_selector, date)
                    self.destroy()
                else:
                    continue

        if not available_teetime:
            self.__quit_driver(driver)
            return False
        else:
            self.__quit_driver(driver)
            return True

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
            if self.process(booking_url):
                # Send message to telegram
                send_message(self.message)
                print_log('Send message to telegram successfully')
                self.logger.emit('Send message to telegram successfully', 'green')

            if self._is_running:
                time.sleep(check_period * 60)
            else:
                self.logger.emit('Crawler stopped', 'green')

    def destroy(self):
        self._is_running = False
        self.logger.emit('Stopping crawler ...', 'red')
        self.finished.emit()
