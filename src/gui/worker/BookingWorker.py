import argparse
import os
import subprocess
import sys
import time
import json

# Add sys path of the project
sys.path.append(os.path.join(os.getcwd()))

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


class BookingWorker():
    def __init__(self, args):
        self.headless = True if args.headless == 'True' else False
        self.day = args.day
        self.selector = args.selector
        self.credential_mode = args.credential_mode

    def __quit_driver(self, driver) -> None:
        driver.quit()
        try:
            subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)
        except Exception as e:
            print_log(e)

    def move_to_day(self, driver, css_selector) -> None:
        try:
            date_button = WebDriverWait(driver, 20).until(
                lambda x: x.find_element(By.CSS_SELECTOR, css_selector))
            date_button.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'rightlist')))
        except Exception as e:
            print_log(e)
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

                signin.fill(
                    driver=driver,
                    email=data['email'],
                    password=data['password']
                )

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
                self.__quit_driver(driver)

    def run(self, booking_url):
        browser = UserActivity(headless=self.headless)
        driver = browser.driver

        # Open Sign In page
        try:
            driver.get(SIGNIN_URL)
        except Exception as e:
            print_log(e)
            self.__quit_driver(driver)

        # Pass the credential
        using_credential_info = self.credential_passing(driver)

        # Open the booking page
        try:
            time.sleep(2)

            driver.get(booking_url)

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
        except Exception as e:
            print_log(e)
            self.__quit_driver(driver)

        # Choose Riverway options
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'courses-selection')))

            time.sleep(1)

            print_log('Choosing Riverway option ...')
            with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'Riverway.js'), 'r', encoding='utf8') as f:
                js = f.read()
            driver.execute_script(js)
        except Exception as e:
            print_log(e)
            self.__quit_driver(driver)

        # Choose the 4 player button
        try:
            print_log('Choosing 4 players option ...')
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'mat-button-toggle-4-button')))

            time.sleep(1)

            four_player_button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.ID, 'mat-button-toggle-4-button'))
            four_player_button.click()
        except Exception as e:
            print_log(e)
            self.__quit_driver(driver)

        time.sleep(5)

        self.__quit_driver(driver)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--credential_mode', choices=['signin', 'signup'],
                        required=True, help='Credential mode (signin or signup)')
    parser.add_argument('--headless', type=str, choices=["True", "False"],
                        required=True, help='Headless mode ("True" or "False")')
    parser.add_argument('--day', type=int, required=True, help='Day in the month')
    parser.add_argument('--selector', type=str, required=True, help='CSS selector of the date button')

    args = parser.parse_args()

    worker = BookingWorker(args)

    # Load configuration
    config_path = os.path.join(os.getcwd(), 'configuration', 'crawler.json')
    with open(config_path, 'r', encoding='utf8') as f:
        config = json.load(f)
        check_period = config['check_period']  # In minutes
        start_time = config['start_time']  # In 24h format
        end_time = config['end_time']  # In 24h format
    # Constant URL
    booking_url = f"https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin={start_time}&TeeOffTimeMax={end_time}"

    worker.run(booking_url)
