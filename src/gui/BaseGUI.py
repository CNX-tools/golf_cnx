import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from abc import abstractmethod


class BaseGUI(QWidget):
    reservation_detail_dir = os.path.join(os.getcwd(), 'assets', 'reservation.csv')

    def __init__(self, MainWindow) -> None:
        super(BaseGUI, self).__init__()
        self.main_window = MainWindow

        # ------------------- Font -------------------
        self.font = QFont()
        self.font.setPointSize(11)

        self.font1 = QFont()
        self.font1.setPointSize(12)
        self.font1.setBold(True)
        self.font1.setWeight(75)

        self.font2 = QFont()
        self.font2.setPointSize(11)
        self.font2.setBold(True)
        self.font2.setWeight(75)

        # ------------------- App Name -------------------
        self.app_name = QLabel(self)
        self.app_name.setObjectName(u"app_name")
        self.app_name.setGeometry(QRect(44, 16, 191, 31))
        self.app_name.setFont(self.font1)

        # ------------------- Lines -------------------
        self.line_1 = QFrame(self)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setGeometry(QRect(270, -2, 3, 61))
        self.line_1.setFrameShape(QFrame.VLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.line_2 = QFrame(self)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(-21, 50, 292, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.line_3 = QFrame(self)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(-20, 90, 292, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.line_4 = QFrame(self)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(262, 100, 20, 561))
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        # ------------------- Left Menu -------------------

        self.get_home_button = QPushButton(self)
        self.get_home_button.setObjectName(u"get_home_button")
        self.get_home_button.setGeometry(QRect(-1, 98, 274, 50))
        self.get_home_button.setFont(self.font)

        # self.telegram_bot_settings_button = QPushButton(self)
        # self.telegram_bot_settings_button.setObjectName(u"telegram_bot_settings_button")
        # self.telegram_bot_settings_button.setGeometry(QRect(-1, 147, 274, 50))
        # self.telegram_bot_settings_button.setFont(self.font)

        self.start_button = QPushButton(self)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(80, 460, 111, 51))
        self.start_button.setFont(self.font2)
        self.start_button.clicked.connect(self.run_crawler)

        self.headless_crawl_checkBox = QCheckBox(self)
        self.headless_crawl_checkBox.setObjectName(u"headless_crawl_checkBox")
        self.headless_crawl_checkBox.setGeometry(QRect(30, 300, 201, 41))
        self.headless_crawl_checkBox.setFont(self.font2)
        self.headless_crawl_checkBox.setChecked(True)

        self.headless_booking_checkBox = QCheckBox(self)
        self.headless_booking_checkBox.setObjectName(u"headless_booking_checkBox")
        self.headless_booking_checkBox.setGeometry(QRect(30, 350, 221, 41))
        self.headless_booking_checkBox.setFont(self.font2)
        self.headless_booking_checkBox.setChecked(True)

        # ------------------- Logs -------------------

        self.logs_output = QPlainTextEdit(self)
        self.logs_output.setObjectName(u"logs_output")
        self.logs_output.setGeometry(QRect(290, 460, 821, 181))
        self.logs_output.setFont(self.font)
        self.logs_output.setReadOnly(True)

        self.logs_label = QLabel(self)
        self.logs_label.setObjectName(u"logs_label")
        self.logs_label.setGeometry(QRect(290, 420, 61, 31))
        self.logs_label.setFont(self.font2)

        self.clear_logs_button = QPushButton(self)
        self.clear_logs_button.setObjectName(u"clear_logs_button")
        self.clear_logs_button.setGeometry(QRect(340, 420, 90, 30))
        self.clear_logs_button.setFont(self.font)
        self.clear_logs_button.clicked.connect(self.clear_logs_button_clicked)

        # ------------------- Credential Mode -------------------

        self.sign_in_radioButton = QRadioButton(self)
        self.sign_in_radioButton.setObjectName(u"sign_in_radioButton")
        self.sign_in_radioButton.setGeometry(QRect(490, 35, 71, 23))
        self.sign_in_radioButton.setFont(self.font)
        self.sign_in_radioButton.clicked.connect(self.sign_in_button_clicked)

        self.sign_up_radioButton = QRadioButton(self)
        self.sign_up_radioButton.setObjectName(u"sign_up_radioButton")
        self.sign_up_radioButton.setGeometry(QRect(590, 35, 71, 23))
        self.sign_up_radioButton.setFont(self.font)
        self.sign_up_radioButton.clicked.connect(self.sign_up_button_clicked)

        self.credential_mode_label = QLabel(self)
        self.credential_mode_label.setObjectName(u"credential_mode_label")
        self.credential_mode_label.setGeometry(QRect(330, 30, 130, 31))
        self.credential_mode_label.setFont(self.font2)

        # ------------------- View Detail Reservation -------------------

        self.view_reservation_button = QCommandLinkButton(self)
        self.view_reservation_button.setObjectName(u"view_reservation_button")
        self.view_reservation_button.setGeometry(QRect(580, 310, 300, 41))
        self.view_reservation_button.setFont(self.font2)
        self.view_reservation_button.clicked.connect(self.view_reservation_button_clicked)

        # Retranslate UI
        self.retranslate_baseUI()

    def retranslate_baseUI(self):
        self.app_name.setText(QCoreApplication.translate("Form", u"Golf Auto Booking Bot", None))
        self.get_home_button.setText(QCoreApplication.translate("Form", u"Home", None))
        self.start_button.setText(QCoreApplication.translate("Form", u"START", None))
        self.logs_label.setText(QCoreApplication.translate("Form", u"Logs", None))
        self.clear_logs_button.setText(QCoreApplication.translate("Form", u"Clear", None))
        # self.telegram_bot_settings_button.setText(QCoreApplication.translate("Form", u"Telegram Bot Setting", None))
        self.credential_mode_label.setText(QCoreApplication.translate("Form", u"Credential Mode :", None))
        self.view_reservation_button.setText(QCoreApplication.translate(
            "Form", u"Click here to view reservation details", None))
        self.sign_in_radioButton.setText(QCoreApplication.translate("Form", u"Sign In", None))
        self.sign_up_radioButton.setText(QCoreApplication.translate("Form", u"Sign Up", None))

        self.headless_crawl_checkBox.setText(QCoreApplication.translate("Form", u"Headless in Crawl Mode", None))
        self.headless_booking_checkBox.setText(QCoreApplication.translate("Form", u"Headless in Booking Mode", None))

    def view_reservation_button_clicked(self):
        # Open browser to view reservation details
        reservation_info_url = 'https://docs.google.com/spreadsheets/d/1MZ7XPcLXAs0GDxYprF6xlHEsqD2_8mmEOaG-0aIbR3g/edit#gid=1168958722'
        QDesktopServices.openUrl(QUrl(reservation_info_url))

    def clear_logs_button_clicked(self):
        self.logs_output.clear()

    def update_log(self, text: str, color: str = 'black'):
        # Get the current date and time in a user-friendly format
        current_datetime = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        # Prepare the log entry with the formatted date and time
        new_log = f'[{current_datetime}] {text}'
        # Apply appropriate HTML formatting
        formatted_log = f'<p style="color:{color}; margin: 0;">{new_log}</p>'
        # Append the formatted log entry to the log output
        self.logs_output.appendHtml(formatted_log)
        # Scroll to the bottom of the log output
        self.logs_output.verticalScrollBar().setValue(self.logs_output.verticalScrollBar().maximum())

    def update_log_horizontal_line(self):
        self.logs_output.appendHtml('-' * 150)
        self.logs_output.verticalScrollBar().setValue(self.logs_output.verticalScrollBar().maximum())

    def sign_in_button_clicked(self):
        self.main_window.setCurrentIndex(0)
        self.sign_up_radioButton.setChecked(True)

    def sign_up_button_clicked(self):
        self.main_window.setCurrentIndex(1)
        self.sign_in_radioButton.setChecked(True)

    @abstractmethod
    def retranlate_UI(self):
        pass

    @abstractmethod
    def run_crawler(self):
        pass
