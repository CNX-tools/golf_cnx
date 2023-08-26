# Test booking
import os
import subprocess
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import UserActivity
import src.utils.SigninUtils as signin
from src.utils.PrintUtils import print_log

browser = UserActivity(headless=False)
driver = browser.driver

# Constant URL
SIGNIN_URL = "https://golfburnaby.cps.golf/onlineresweb/auth/verify-email"
BOOKING_URL = "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23"


def quit_driver(driver):
    driver.quit()
    subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)
    sys.exit()


# Open the page
try:
    driver.maximize_window()
    driver.get(SIGNIN_URL)
    # Wait until the page is loaded
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, 'email')))
except Exception as e:
    print_log(e)
    quit_driver(driver)

# Fill the form
try:
    time.sleep(2)
    signin.fill(driver, email='minhquan052003@gmail.com', password='Mkdabihack@123')
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
except Exception as e:
    print(e)
    quit_driver(driver)

# Open the booking page
try:
    time.sleep(5)
    driver.get(BOOKING_URL)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
except Exception as e:
    print(e)
    quit_driver(driver)

# Choose Riverway options
try:
    time.sleep(2)
    with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'Riverway.js'), 'r', encoding='utf8') as f:
        js = f.read()
    driver.execute_script(js)
except Exception as e:
    print(e)
    quit_driver(driver)

# Choose the 4 player button
try:
    time.sleep(1)
    four_player_button = driver.find_element(By.CSS_SELECTOR, '#mat-button-toggle-4-button')
    four_player_button.click()
except Exception as e:
    print(e)
    quit_driver(driver)

# Get the current active date from execute script
try:
    time.sleep(1)
    with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'GetActiveDate.js'), 'r', encoding='utf8') as f:
        js = f.read()
    current_active_dates = driver.execute_script(js)
except Exception as e:
    print(e)
    quit_driver(driver)

# Iterate through the dates, check whether exist any session available
for css_selector, date in current_active_dates:
    time.sleep(3)
    print('Checking date: ' + date)
    date_button = driver.find_element(By.CSS_SELECTOR, css_selector)
    date_button.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'leftfilter')))

    # Check whether there is any available session
    available_session_button = driver.find_elements(By.CLASS_NAME, 'btnStepper')
    if len(available_session_button) == 0:
        print('No available session in date:' + date)
        continue
    else:
        print('Found available session in date:' + date)
        print(available_session_button)

    print('-' * 50)


time.sleep(10000)
quit_driver(driver)
