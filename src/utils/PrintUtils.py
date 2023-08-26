from datetime import datetime
from PyQt5.QtWidgets import QPlainTextEdit


def print_log(message):
    date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{date_and_time}]: {message}')
