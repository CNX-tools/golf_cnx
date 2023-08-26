import time
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def fill(driver: Chrome, email: str, first_name: str, last_name: str, pass_word: str, phone: str):
    # Fill email:
    email_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-0')
    email_input.send_keys(email)

    time.sleep(0.2)

    # Fill first name:
    first_name_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-1')
    first_name_input.send_keys(first_name)

    time.sleep(0.2)

    # Fill last name:
    last_name_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-2')
    last_name_input.send_keys(last_name)

    time.sleep(0.2)

    # Fill password:
    password_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-3')
    password_input.send_keys(pass_word)

    time.sleep(0.2)

    # Fill confirm password:
    confirm_password_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-4')
    confirm_password_input.send_keys(pass_word)

    time.sleep(0.2)

    # Fill phone:
    phone_input = driver.find_element(By.CSS_SELECTOR, '#mat-input-5')
    phone_input.send_keys(phone)

    time.sleep(1)

    # Hit enter
    phone_input.send_keys(Keys.ENTER)
