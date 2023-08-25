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
BOOKING_URL = "https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin=0&TeeOffTimeMax=23"


def quit_driver(driver):
    driver.quit()
    subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)


# Open the booking page
try:
    driver.get(BOOKING_URL)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
except Exception as e:
    print(e)
    quit_driver(driver)

time.sleep(4)

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

# Iterate through the dates, check whether exist any session available
for css_selector, date in current_active_dates:
    print('Checking date: ' + date)
    try:
        date_button = driver.find_element(By.CSS_SELECTOR, css_selector)
        date_button.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'leftfilter')))
    except Exception as e:
        print(e)
        quit_driver(driver)

    time.sleep(4.5)

    try:
        driver.execute_script('''
                            const matSelect = document.querySelector('.teetimetable');
                            matSelect.click();
                            ''')
        break
    except JavascriptException as e:
        print(e)
        pass

time.sleep(10000)
quit_driver(driver)
