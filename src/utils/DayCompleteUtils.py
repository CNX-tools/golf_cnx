from datetime import datetime

from src.utils.GoogleSheetUtils import read_data
import pandas as pd


def get_day_complete_string(input_day: int) -> str:
    """
    Get the day, add month and year to it, and return the result as a string
    Args:
        input_day (int): Day of the month

    Returns:
        str: A string of the date in format 'YYYY-MM-DD'
    """

    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year

    # If the input day is less than the current day, add 1 month to the current month
    if input_day < day:
        month += 1

    # Handle for the case input day is greater 1 and today is the last day of the december
    if input_day < day and (input_day >= 1 and month == 12):
        year += 1
        month = 1

    # Get the correct format of the date
    if month < 10:
        month = f'0{month}'
    if input_day < 10:
        input_day = f'0{input_day}'

    return f'{year}-{month}-{input_day}'


def whether_day_has_reservation_before(input_day: int, email: str) -> bool:
    """
    Check whether the day has reservation before together with the email
    Args:
        input_day (int): Day of the month

    Returns:
        bool: True if the day has reservation before, False otherwise
    """
    # Get the day complete string
    day_complete_string = get_day_complete_string(input_day)

    # Get the data from google sheet
    data = read_data()

    # Check whether the day has reservation before together with the email
    for index, row in data.iterrows():
        if row['date'] == day_complete_string and row['email'] == email:
            return True

    return False
