# Test booking
import json
import os
import subprocess
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.utils.TelegramBot import send_message
from src.utils.PrintUtils import print_log
from src.utils.SeleniumUtils import UserActivity


def quit_driver(driver):
    driver.quit()
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chromium.exe"], check=True)
    except Exception as e:
        pass


def move_to_next_day(driver, css_selector):
    try:
        date_button = WebDriverWait(driver, 20).until(
            lambda x: x.find_element(By.CSS_SELECTOR, css_selector))
        date_button.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'rightlist')))
    except Exception as e:
        print_log(e)
        quit_driver(driver)


def check_available_teetime(driver):
    try:
        no_teetime = WebDriverWait(driver, 30).until(
            lambda x: x.find_element(By.CLASS_NAME, 'divNoTeeTime'))
        return False
    except Exception as e:
        return True


def check_for_each_day(driver, date):
    global message
    if check_available_teetime(driver):
        # Try to click the first available session on this date
        try:
            button = WebDriverWait(driver, 30).until(
                lambda x: x.find_element(By.CLASS_NAME, 'btnStepper'))
            session_info = button.text.split('\n')
            session_info.extend(session_info[1].split(' | '))
            del session_info[1]
            print_log(f'Found available tee time on date {date}: {session_info}')
            message += f'Found available tee time on date {date}: {session_info}\n\n'
            return True
        except Exception as e:
            print_log(f'Cannot click the first available session with error: {e}')
            return False
    else:
        print_log(f'No available tee time on date {date}')
        return False


def process(booking_url):
    global message
    current_active_dates = []
    browser = UserActivity(headless=True)
    driver = browser.driver
    # Open the booking page
    try:
        print_log(f'Opening booking page: {booking_url}')
        driver.get(booking_url)
    except Exception as e:
        print_log('Timeout, trying again ...')
        driver.refresh()

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
        print(e)
        quit_driver(driver)

    # Choose the 4 player button
    try:
        time.sleep(1)
        print_log('Choosing 4 players option ...')
        four_player_button = WebDriverWait(driver, 30).until(
            lambda x: x.find_element(By.ID, 'mat-button-toggle-4-button'))
        four_player_button.click()
    except Exception as e:
        print(e)
        quit_driver(driver)

    # Get the current active date from execute script
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-calendar-container')))
        time.sleep(1)
        with open(os.path.join(os.getcwd(), 'src', 'utils', 'javascript', 'GetActiveDate.js'), 'r', encoding='utf8') as f:
            js = f.read()
        current_active_dates = driver.execute_script(js)

        dates = [date for _, date in current_active_dates]

        print_log(f'Current active dates: {", ".join(dates)}')
        message += f'Current active dates: {", ".join(dates)}\n\n'

    except Exception as e:
        print_log(e)
        quit_driver(driver)

    time.sleep(1)

    available_teetime = False
    # Iterate through the dates, check whether exist any session available
    for css_selector, date in current_active_dates:
        print_log(f'Checking date: {date}')
        move_to_next_day(driver, css_selector)
        time.sleep(2)
        check_result = check_for_each_day(driver, date)
        if check_result:
            available_teetime = True
        else:
            continue

    if not available_teetime:
        quit_driver(driver)
        return False
    else:
        quit_driver(driver)
        return True


def main():
    # Load configuration
    config_path = os.path.join(os.getcwd(), 'configuration', 'crawler.json')
    with open(config_path, 'r', encoding='utf8') as f:
        config = json.load(f)
        check_period = config['check_period']  # In minutes
        start_time = config['start_time']  # In 24h format
        end_time = config['end_time']  # In 24h format
    # Constant URL
    booking_url = f"https://golfburnaby.cps.golf/onlineresweb/search-teetime?TeeOffTimeMin={start_time}&TeeOffTimeMax={end_time}"

    # Run the crawler in a loop with a period of 5 minutes
    while True:
        print('-' * 120)
        print_log(f'Start checking with time frame: {start_time}h - {end_time}h  - Riverway - 4 players')
        # Text to telegram
        message = ''
        message += f'Start checking with time frame: {start_time}h - {end_time}h - Riverway - 4 players\n\n'
        if process(booking_url):
            # Send message to telegram
            send_message(message)
            print_log('Send message to telegram successfully')
        time.sleep(check_period * 60)
