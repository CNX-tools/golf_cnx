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
        return

    if current_url == r'https://golfburnaby.cps.golf/onlineresweb/auth/login':
        print_log('The user has already registered. Loggin in ...')

        # Fill password:
        password_input = WebDriverWait(driver, 30).until(
            lambda x: x.find_element(By.NAME, 'password'))
        password_input.send_keys(password)

        # Hit enter
        password_input.send_keys(Keys.ENTER)

        time.sleep(1.5)

        if EC.presence_of_all_elements_located((By.CLASS_NAME, 'error-message')) is not False:
            print_log('The password is not correct ...')
            return
        else:
            print_log('Login successfully ...')
            return
