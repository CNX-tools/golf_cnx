import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from PrintUtils import print_log

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


data = read_data()
print(data.head())
