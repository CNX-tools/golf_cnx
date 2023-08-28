import os
import subprocess
import sys
import time
import json

# Add sys path of the project
sys.path.append(os.path.join(os.getcwd()))

from PyQt5.QtCore import QObject, pyqtSignal

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.utils.SeleniumUtils import UserActivity
import src.utils.SigninUtils as signin
import src.utils.SignupUtils as signup
from src.utils.PrintUtils import print_log
from src.utils.GetInfoUtils import get_random_info

# Constant URL
SIGNIN_URL = "https://golfburnaby.cps.golf/onlineresweb/auth/verify-email"


class BookingWorker(QObject):
    finished = pyqtSignal()
    started = pyqtSignal()
    logger = pyqtSignal(str, str)

    def __init__(self, headless, day, css_selector, credential_mode, parent=None) -> None:
        super(BookingWorker, self).__init__(parent)
        self.headless = headless
        self.day = day
        self.css_selector = css_selector
        self.credential_mode = credential_mode

    def __quit_driver(self, driver) -> None:
        try:
            driver.quit()
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)
            self.finished.emit()
            print_log('The booking procedure is finished ...')
            self.logger.emit('The booking procedure is finished ...', 'green')
        except Exception as e:
            self.logger.emit(str(e), 'red')
            print_log(e)

    def move_to_day(self, driver, css_selector) -> None:
        try:
            print_log(f'Move to the day button with css selector is {css_selector} ...')
            self.logger.emit(f'Move to the day button with css selector is {css_selector} ...', 'black')
            date_button = WebDriverWait(driver, 20).until(
                lambda x: x.find_element(By.CSS_SELECTOR, css_selector))
            date_button.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'rightlist')))
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

    def check_available_teetime(self, driver) -> bool:
        try:
            no_teetime = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CLASS_NAME, 'divNoTeeTime'))
            return False
        except Exception as e:
            return True

    def credential_passing(self, driver) -> dict:
        """
            Pass the credential to the form (sign in or sign up) and return the used data
        """
        if self.credential_mode == 'signin':
            # Get the credential data
            data_dir = os.path.join(os.getcwd(), 'data', 'sign_in.json')
            with open(data_dir, 'r') as f:
                data = json.load(f)

            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.NAME, 'email')))
                time.sleep(1.5)

                account_status = signin.fill(
                    driver=driver,
                    email=data['email'],
                    password=data['password']
                )

                if account_status is False:
                    print_log('Problem with the account. Please check again ...')
                    self.logger.emit('Problem with the account. Please check again ...', 'red')
                    self.__quit_driver(driver)
                    return None
                else:
                    print_log('The account is valid ...')
                    self.logger.emit('The account is valid ...', 'green')

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))

                return {
                    'email': data['email'],
                    'password': data['password'],
                    'first_name': '',
                    'last_name': '',
                    'phone': ''
                }

            except Exception as e:
                print_log(e)
                self.logger.emit(str(e), 'red')
                self.__quit_driver(driver)
        else:
            # Get the credential data
            data_dir = os.path.join(os.getcwd(), 'data', 'sign_up.json')
            with open(data_dir, 'r') as f:
                data = json.load(f)

            try:
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.NAME, 'email')))
                time.sleep(1.5)

                random_info = get_random_info()

                signup.fill(
                    driver=driver,
                    email=random_info['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    password=random_info['password'],
                    phone=random_info['phone']
                )

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))

                return {
                    'email': random_info['email'],
                    'password': random_info['password'],
                    'first_name': data['first_name'],
                    'last_name': data['first_name'],
                    'phone': random_info['phone']
                }
            except Exception as e:
                print_log(e)
                self.logger.emit(str(e), 'red')
                self.__quit_driver(driver)

    def store_reservation_info(self, session_info) -> None:
        # Store the reservation info
        reservation_dir = os.path.join(os.getcwd(), 'data', 'reservation.csv')

        # Building the reservation info
        name = f"{self.using_credential_info['first_name']} {self.using_credential_info['last_name']}"

        reservation_info = [self.day,
                            self.using_credential_info['email'],
                            self.using_credential_info['password'],
                            name]

        reservation_info.extend(session_info)

        info_string = ','.join(reservation_info)

        with open(reservation_dir, 'a', encoding='utf8') as f:
            f.write(info_string + '\n')

    def make_reservation(self, driver) -> None:
        try:
            # CLick the first teetime button
            teetime_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CLASS_NAME, 'btnStepper'))
            session_info = teetime_button.text.split('\n')
            session_info.extend(session_info[1].split(' | '))
            del session_info[1]

            teetime_button.click()

            time.sleep(1)

            # Check whether the element with class name "mat-dialog-title" exist or not (Has booked before)
            booked_message = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'mat-dialog-title')))

            if booked_message.is_displayed():
                print_log(f'There has been a reservation in day {self.day} before ...')
                self.logger.emit(f'There has been a reservation in day {self.day} before ...', 'red')
                self.__quit_driver(driver)

            # Passing Agreement Policy
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.mat-focus-indicator.full-width.btn-action.mat-raised-button.mat-button-base.mat-primary')))
            next_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CSS_SELECTOR, 'button.mat-focus-indicator.full-width.btn-action.mat-raised-button.mat-button-base.mat-primary'))
            next_button.click()

            time.sleep(1)

            # Click the final button
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.mat-focus-indicator.large-button.button-continue.mat-flat-button.mat-button-base.mat-primary.ng-star-inserted')))
            final_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CSS_SELECTOR, 'button.mat-focus-indicator.large-button.button-continue.mat-flat-button.mat-button-base.mat-primary.ng-star-inserted'))
            final_button.click()

            time.sleep(3)
            # Check whether the element with class name "mat-card-title" exist or not
            success_message = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'mat-card-title')))

            if success_message.is_displayed():
                print_log('The reservation is successful ...')
                self.logger.emit('The reservation is successful ...', 'green')
                self.store_reservation_info(session_info)
                self.__quit_driver(driver)

            else:
                print_log('The reservation is failed ...')
                self.logger.emit('The reservation is failed ...', 'red')
                self.__quit_driver(driver)
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

    def process(self, booking_url):
        browser = UserActivity(headless=self.headless)
        driver = browser.driver

        # Open Sign In page
        try:
            driver.get(SIGNIN_URL)
            print_log('Opening Signin page ...')
            self.logger.emit('Opening Signin page ...', 'black')
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Pass the credential
        self.using_credential_info = self.credential_passing(driver)

        if self.using_credential_info is None:
            return

        # Open the booking page
        try:
            time.sleep(2)
            driver.get(booking_url)
            print_log(f'Opening booking page: {booking_url}')
            self.logger.emit(f'Opening booking page: {booking_url}', 'black')
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Choose Riverway options
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
        try:
            print_log('Choosing 4 players option ...')
            self.logger.emit('Choosing 4 players option ...', 'black')
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'mat-button-toggle-4-button')))

            time.sleep(1)

            four_player_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.ID, 'mat-button-toggle-4-button'))
            four_player_button.click()
        except Exception as e:
            print_log(e)
            self.logger.emit(str(e), 'red')
            self.__quit_driver(driver)

        # Click the date button
        time.sleep(3)
        self.move_to_day(driver, self.css_selector)

        # Check whether the teetime is available or not
        available_teetime = self.check_available_teetime(driver)

        if available_teetime:  # Has teetime button
            print_log('Teetime available ...')
            self.logger.emit('Teetime available ...', 'green')
            self.make_reservation(driver)
        else:
            print_log('No teetime available ...')
            self.logger.emit('No teetime available ...', 'red')
            self.__quit_driver(driver)

    def run(self):
        config_path = os.path.join(os.getcwd(), 'configuration', 'crawler.json')
        with open(config_path, 'r', encoding='utf8') as f:
            config = json.load(f)
            start_time = config['start_time']  # In 24h format
            end_time = config['end_time']  # In 24h format

        # Constant URL
        booking_url = f"https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin={start_time}&TeeOffTimeMax={end_time}"
        self.started.emit()
        self.process(booking_url)
