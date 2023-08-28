import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.PrintUtils import print_log

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

try:
    secret_file = os.path.join(os.getcwd(), 'assets', 'secret-key.json')
except:
    print_log('Please put your secret-key.json file in the assets folder')

creds = ServiceAccountCredentials.from_json_keyfile_name(filename=secret_file, scopes=scopes)

files = gspread.authorize(creds)


def read_data() -> pd.DataFrame:
    """
    Read the data from the spreadsheet 'reservation' and return a pandas DataFrame

    Sample data:
    | date | email | password | name | tjme | price (1 person) | holes | players |
    | ---- | ----- | -------- | ---- | ---- | ---------------- | ----- | ------- |

    Returns:
        pd.DataFrame: A pandas DataFrame
    """
    # Open the workbook
    workbook = files.open('reservation')

    # Get all sheets
    sheet = workbook.sheet1

    # Using pandas to read the data
    data = pd.DataFrame(sheet.get_all_records())

    return data


def update_data(data: dict):
    """
    Update the data to the spreadsheet 'reservation'

    Args:
        data (dict): A dictionary of data to update

        Example:
        {
            'date': '2023-08-28',
            'email': 'example@gmail.com',
            'password': 'example',
            'name': 'Example',
            'time': '12:01 PM',
            'price (1 person)': 'CA$50',
            'holes': '18 HOLES',
            'players': '2-4 GOLFERS'
        }
    """
    # Open the workbook
    workbook = files.open('reservation')

    # Get all sheets
    sheet = workbook.sheet1

    # Update the data
    sheet.append_row(list(data.values()))

    # Call the sheet to sort the data by the column 'date' in asc order except the first row
    sheet.sort((1, 'asc'), range='A2:H10000')


# data = {
#     'date': '2023-08-01',
#     'email': 'example@gmail.com',
#     'password': 'example',
#     'name': 'Example',
#     'time': '12:01 PM',
#     'price (1 person)': 'CA$50',
#     'holes': '18 HOLES',
#     'players': '2-4 GOLFERS'
# }
# update_data(data)
