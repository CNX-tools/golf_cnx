import json
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from src.gui.BaseGUI import BaseGUI
from src.gui.worker.CrawlerWorker import CrawlerWorker
from src.gui.worker.BookingWorker import BookingWorker


class SignupGUI(BaseGUI):
    crawler_thread = QThread()
    booking_thread = QThread()

    def __init__(self, MainWindow) -> None:
        super(SignupGUI, self).__init__(MainWindow)

        self.sign_up_radioButton.setChecked(True)

        # self.book_button = QPushButton(self)
        # self.book_button.setObjectName(u"book_button")
        # self.book_button.setGeometry(QRect(80, 550, 111, 51))
        # self.book_button.setFont(self.font)
        # self.book_button.clicked.connect(lambda: self.run_booking_procedure('.day-unit:nth-child(32)', '30'))

        self.retranlate_UI()

    def retranlate_UI(self):
        pass
        # self.book_button.setText(QCoreApplication.translate("Form", u"Booking", None))

    def run_crawler(self):
        try:
            if self.crawler_thread.isRunning():
                self.crawler.destroy()

            self.crawler = CrawlerWorker(self.headless_crawl_checkBox.isChecked(), credential_mode='signup')
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
            self.booker = BookingWorker(self.headless_booking_checkBox.isChecked(), date, css_selector, 'signup')
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
