# Test booking
import os
import subprocess
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException

from src.utils.SeleniumUtils import UserActivity
from src.utils.SignupUtils import fill
from src.utils.GetInfoUtils import get_random_info

browser = UserActivity()
driver = browser.driver

# Constant URL
REGISTER_URL = "https://golfburnaby.cps.golf/onlineresweb/auth/register"
# BOOKING_URL = "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=9&TeeOffTimeMax=15"
BOOKING_URL = "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=9&TeeOffTimeMax=20"


def quit_driver(driver):
    driver.quit()
    subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)


def move_to_next_day(driver, css_selector):
    try:
        date_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.CSS_SELECTOR, css_selector))
        date_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'rightlist')))
    except Exception as e:
        print(e)
        quit_driver(driver)


def check_available_teetime(driver):
    try:
        no_teetime = WebDriverWait(driver, 3).until(
            lambda x: x.find_element(By.CLASS_NAME, 'divNoTeeTime'))

        return False
    except Exception as e:
        return True


def check_for_each_day(driver, date):
    if check_available_teetime(driver):
        print(f'Found available tee time on date {date}')

        # Try to click the first available session on this date
        try:
            button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element(By.CLASS_NAME, 'teetimetable'))
            button.click()
            return True
        except Exception as e:
            print(f'Cannot click the first available session with error: {e}')
            return False
    else:
        return False


if __name__ == '__main__':
    # Open the booking page
    try:
        driver.get(BOOKING_URL)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'rightlist')))
    except Exception as e:
        print(e)
        quit_driver(driver)

    time.sleep(5)

    # Get the current active date from execute script
    try:
        with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'GetActiveDate.js'), 'r', encoding='utf8') as f:
            js = f.read()
        current_active_dates = driver.execute_script(js)
        print(current_active_dates)
    except Exception as e:
        print(e)
        quit_driver(driver)

    time.sleep(2)

    available_teetime = False
    # Iterate through the dates, check whether exist any session available
    for css_selector, date in current_active_dates:
        print('Checking date:' + date)
        move_to_next_day(driver, css_selector)
        time.sleep(2)
        check_result = check_for_each_day(driver, date)
        if check_result:
            available_teetime = True
            break
        else:
            print('No available tee time on date ' + date)
            continue

    if not available_teetime:
        print('No available tee time found')
        quit_driver(driver)
    else:
        time.sleep(10000)
        quit_driver(driver)
