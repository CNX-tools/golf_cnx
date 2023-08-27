import json
import os
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from src.gui.BaseGUI import BaseGUI
from src.gui.worker.CrawlerWorker import CrawlerWorker


class SiginGUI(BaseGUI):
    data_dir = os.path.join(os.getcwd(), 'data', 'sign_in.json')
    with open(data_dir, 'r') as f:
        data = json.load(f)

    crawler_thread = QThread()

    def __init__(self, MainWindow) -> None:
        super(SiginGUI, self).__init__(MainWindow)

        self.sign_in_radioButton.setChecked(True)

        self.email_label = QLabel(self)
        self.email_label.setObjectName(u"email_label")
        self.email_label.setGeometry(QRect(410, 100, 51, 31))
        self.email_label.setFont(self.font2)

        self.password_label = QLabel(self)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(380, 170, 81, 31))
        self.password_label.setFont(self.font2)

        self.email_lineEdit = QLineEdit(self)
        self.email_lineEdit.setObjectName(u"email_lineEdit")
        self.email_lineEdit.setGeometry(QRect(480, 100, 481, 31))
        self.email_lineEdit.setFont(self.font)
        self.email_lineEdit.setText(self.data['email'])
        self.email_lineEdit.textChanged.connect(self.update_data)

        self.password_lineEdit = QLineEdit(self)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setGeometry(QRect(480, 170, 481, 31))
        self.password_lineEdit.setFont(self.font)
        self.password_lineEdit.setText(self.data['password'])
        self.password_lineEdit.textChanged.connect(self.update_data)
        self.password_lineEdit.setEchoMode(QLineEdit.Password)

        self.show_password_button = QPushButton(self)
        self.show_password_button.setObjectName(u"show_password_button")
        self.show_password_button.setGeometry(QRect(959, 169, 51, 33))
        self.show_password_button.setFont(self.font)
        self.show_password_button.clicked.connect(lambda: self.password_lineEdit.setEchoMode(
            QLineEdit.Normal) if self.password_lineEdit.echoMode() == QLineEdit.Password else self.password_lineEdit.setEchoMode(QLineEdit.Password))

        self.retranlate_UI()

    def retranlate_UI(self):
        self.email_label.setText(QCoreApplication.translate("self", u"Email :", None))
        self.password_label.setText(QCoreApplication.translate("self", u"Password :", None))
        self.show_password_button.setText(QCoreApplication.translate("Form", u"Show", None))

    def update_data(self):
        self.data['email'] = self.email_lineEdit.text()
        self.data['password'] = self.password_lineEdit.text()

        with open(self.data_dir, 'w') as f:
            json.dump(self.data, f)

    def run_crawler(self):
        try:
            if self.crawler_thread.isRunning():
                self.crawler.destroy()

            self.crawler = CrawlerWorker(self.logs_output, self.headless_crawl_checkBox.isChecked())
            self.crawler.moveToThread(self.crawler_thread)
            self.crawler.finished.connect(self.crawler_thread.quit)
            self.crawler.finished.connect(self.crawler.deleteLater)

            # When thread started
            self.crawler_thread.started.connect(self.crawler.run)

            # Connect signals
            self.crawler.start_check.connect(self.update_log_horizontal_line)
            self.crawler.start_check.connect(lambda: self.start_button.setText('STOP'))
            self.crawler.logger.connect(self.update_log)
            self.crawler.start_booking.connect(self.run_booking_procedure)

            # When thread is finished
            self.crawler_thread.finished.connect(lambda: self.start_button.setText('START'))

            # Start thread
            self.crawler_thread.start()
        except:
            pass

    def run_booking_procedure(self, css_selector: str, date: str):
        # Define the command to run
        python_file_dir = os.path.join(os.getcwd(), 'src', 'gui', 'worker', 'BookingWorker.py')
        headless_value = "True" if self.headless_booking_checkBox.isChecked() else "False"
        command = [
            "python",               # Command to run
            python_file_dir,    # Script filename
            "--credential_mode=signin",  # Credential argument with value
            f"--day={int(date)}",        # Dateday argument with value
            f'--selector="{css_selector}"',    # Selector argument with value (enclosed in quotes)
            f'--headless={headless_value}'
        ]

        # Run the command in a new shell
        process = subprocess.Popen(command, shell=True)

        # # Wait for the process to finish
        # process.wait()
