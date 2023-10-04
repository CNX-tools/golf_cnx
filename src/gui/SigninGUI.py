import json
import os
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from src.gui.BaseGUI import BaseGUI
from src.gui.worker.CrawlerWorker import CrawlerWorker
from src.gui.worker.BookingWorker import BookingWorker


class SiginGUI(BaseGUI):
    data_dir = os.path.join(os.getcwd(), 'data', 'sign_in.json')
    with open(data_dir, 'r') as f:
        data = json.load(f)

    crawler_thread = QThread()
    booking_thread = QThread()

    def __init__(self, MainWindow, run_status='normal') -> None:
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

        self.book_button = QPushButton(self)
        self.book_button.setObjectName(u"book_button")
        self.book_button.setGeometry(QRect(80, 550, 111, 51))
        self.book_button.setFont(self.font)
        self.book_button.clicked.connect(lambda: self.run_booking_procedure('.day-unit:nth-child(4)', '4'))

        self.retranlate_UI()

        if run_status == 'restart':
            self.start_button.click()

    def retranlate_UI(self):
        self.email_label.setText(QCoreApplication.translate("self", u"Email :", None))
        self.password_label.setText(QCoreApplication.translate("self", u"Password :", None))
        self.show_password_button.setText(QCoreApplication.translate("Form", u"Show", None))
        self.book_button.setText(QCoreApplication.translate("Form", u"Booking", None))

    def update_data(self):
        self.data['email'] = self.email_lineEdit.text()
        self.data['password'] = self.password_lineEdit.text()

        with open(self.data_dir, 'w') as f:
            json.dump(self.data, f)

    def run_crawler(self):
        try:
            if self.crawler_thread.isRunning():
                self.crawler.destroy()

            self.crawler = CrawlerWorker(self.headless_crawl_checkBox.isChecked(), credential_mode='signin')
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
        try:

            self.booker = BookingWorker(self.headless_booking_checkBox.isChecked(), date, css_selector, 'signin')
            self.booker.moveToThread(self.booking_thread)

            self.booker.finished.connect(self.booking_thread.quit)
            self.booker.finished.connect(self.booker.deleteLater)
            self.booker.finished.connect(self.run_crawler)

            # When thread started
            self.booking_thread.started.connect(self.booker.run)

            # Connect signals
            self.booker.started.connect(self.update_log_horizontal_line)
            self.booker.logger.connect(self.update_log)

            # Start thread
            self.booking_thread.start()
        except Exception as e:
            print(e)
            pass
