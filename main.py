# Test booking
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import UserActivity

browser = UserActivity()
driver = browser.driver

# Open the page
try:
    driver.get("https://golfburnaby.cps.golf/onlineresweb/index.html")
    # Wait until the page is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//body/app-root/app-full-layout/div/mat-toolbar/app-header/button')))
except Exception as e:
    print(e)
    driver.quit()
    exit()

# Sign in
try:
    sign_in_button = driver.find_element(
        By.XPATH, "//body/app-root/app-full-layout/div/mat-toolbar/app-header/button")
    sign_in_button.click()
    driver.implicitly_wait(3)
except Exception as e:
    print(e)
    driver.quit()
    exit()

time.sleep(1)
driver.quit()
