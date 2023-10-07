import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os

from bs4 import BeautifulSoup as bs


def main():
    webdriver_service = Service(ChromeDriverManager().install())

    download_directory = os.path.join(os.getcwd(), 'download')

    os.makedirs(download_directory, exist_ok=True)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Optional: Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920x1080")  # Optional: Set window size

    # Set the download directory as a Chrome option
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_directory
    })

    # Create driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    url = "https://finance.vietstock.vn/ket-qua-giao-dich?tab=thong-ke-gia&exchange=1"
    driver.get(url)

    # login web
    print('Clicking login button')
    login1(driver)

    # Cho den khi khung dang nhap hien ra
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "form1")))

    # user_pass
    print('Entering username and password')
    user_pass(driver)

    # click login
    print('Clicking login button')
    login2(driver)

    # download file excel
    print('Clicking export excel button')
    click_excel(driver)

    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # with open('test1.html', 'w', encoding='utf-8') as f:
    #     f.write(driver.page_source)

    # print('Done')


def login1(driver):
    login_button1 = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".title-link.btnlogin-link"))
    )

    time.sleep(2)
    driver.execute_script('''document.querySelector(".title-link.btnlogin-link").click()''')
    time.sleep(2)


def login2(driver):
    login_button2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btnLoginAccount"))
    )

    login_button2.click()

    time.sleep(3)


def user_pass(driver):
    user = WebDriverWait(driver, 20).until(
        lambda x: x.find_element(By.ID, "txtEmailLogin"))
    user.send_keys("thanhtruongtran23@gmail.com")

    time.sleep(1)

    password = WebDriverWait(driver, 20).until(
        lambda x: x.find_element(By.ID, "txtPassword"))
    password.send_keys("truongthanh0812")


def click_excel(driver):
    export_excel_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@title="Export Excel"]')))
    export_excel_link.click()

    time.sleep(2)
# def parse():

#     # Parse the html source using bs4 to get the request verification token
#     with open('test1.html', 'r', encoding='utf-8') as f:
#         soup = bs(f.read(), 'html.parser')

#     verification_token_input = soup.find('input', {'name': '__RequestVerificationToken'})

#     # Get the value attribute of the input element
#     verification_token_value = verification_token_input['value']

#     # Print the verification token value
#     print(verification_token_value)


if __name__ == "__main__":
    main()
    # parse()
