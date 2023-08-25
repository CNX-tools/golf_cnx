# Test booking
import os
import subprocess
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    time.sleep(5)
    driver.get(BOOKING_URL)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'site-name')))
except Exception as e:
    print(e)
    quit_driver(driver)

x_path = '//body/app-root/app-full-layout/div/mat-sidenav-container/mat-sidenav-content/div[1]/app-search-teetime-page/div/div[2]/app-search-teetime-list/div/div[2]/{}/app-search-teetime-item/div/button'
tries = ['div', 'div[1]']


for element in tries:
    try:
        button = driver.find_element(By.XPATH, x_path.format(element))
        button.click()
        break
    except:
        pass

time.sleep(10000)
quit_driver(driver)
