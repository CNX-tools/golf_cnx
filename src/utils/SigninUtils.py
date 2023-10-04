import os
import time
from undetected_chromedriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.PrintUtils import print_log


def fill(driver: Chrome, email: str, password: str):
    # Fill email:
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, 'email')))

    time.sleep(1)

    email_input = WebDriverWait(driver, 30).until(
        lambda x: x.find_element(By.NAME, 'email'))
    email_input.send_keys(email)

    # Hit enter
    time.sleep(0.5)
    email_input.send_keys(Keys.ENTER)

    # Get the current url of the page
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'site-name')))

    time.sleep(2)
    current_url = driver.current_url

    if current_url == r'https://golfburnaby.cps.golf/onlineresweb/auth/register':  # The user hasn't registered yet
        print_log('The user hasn\'t registered yet ...')
        return False

    if current_url == r'https://golfburnaby.cps.golf/onlineresweb/auth/login':
        print_log('The user has already registered. Loggin in ...')

        # Fill password:
        time.sleep(2)
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.NAME, 'password')))
        password_input = WebDriverWait(driver, 30).until(
            lambda x: x.find_element(By.NAME, 'password'))
        password_input.send_keys(password)

        # Hit enter
        password_input.send_keys(Keys.ENTER)

        # Check whether the element with class name "error-message" exist or not
        try:
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'error-message')))
            print_log('The password is incorrect. Please check again ...')
            return False
        except Exception as e:
            print_log('The password is correct ...')
            return True
