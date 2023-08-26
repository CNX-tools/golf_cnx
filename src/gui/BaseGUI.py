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
        self.font.setPointSize(10)

        self.font1 = QFont()
        self.font1.setPointSize(12)
        self.font1.setBold(True)
        self.font1.setWeight(75)

        self.font2 = QFont()
        self.font2.setPointSize(10)
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

        self.telegram_bot_settings_button = QPushButton(self)
        self.telegram_bot_settings_button.setObjectName(u"telegram_bot_settings_button")
        self.telegram_bot_settings_button.setGeometry(QRect(-1, 147, 274, 50))
        self.telegram_bot_settings_button.setFont(self.font)

        self.start_button = QPushButton(self)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setGeometry(QRect(80, 460, 111, 51))
        self.start_button.setFont(self.font2)

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

        # ------------------- Credential Mode -------------------

        self.credential_comboBox = QComboBox(self)
        self.credential_comboBox.addItem("")
        self.credential_comboBox.addItem("")
        self.credential_comboBox.setObjectName(u"credential_comboBox")
        self.credential_comboBox.setGeometry(QRect(480, 30, 151, 31))

        self.credential_mode_label = QLabel(self)
        self.credential_mode_label.setObjectName(u"credential_mode_label")
        self.credential_mode_label.setGeometry(QRect(340, 30, 121, 31))
        self.credential_mode_label.setFont(self.font)

        # ------------------- View Detail Reservation -------------------

        self.view_reservation_button = QCommandLinkButton(self)
        self.view_reservation_button.setObjectName(u"view_reservation_button")
        self.view_reservation_button.setGeometry(QRect(580, 310, 271, 41))
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
        self.telegram_bot_settings_button.setText(QCoreApplication.translate("Form", u"Telegram Bot Setting", None))
        self.credential_comboBox.setItemText(0, QCoreApplication.translate("Form", u"Sign in", None))
        self.credential_comboBox.setItemText(1, QCoreApplication.translate("Form", u"Sign up", None))
        self.credential_mode_label.setText(QCoreApplication.translate("Form", u"Credential Mode:", None))
        self.view_reservation_button.setText(QCoreApplication.translate(
            "Form", u"Click here to view reservation details", None))

    def view_reservation_button_clicked(self):
        # Open reservation detail file with default application
        os.startfile(self.reservation_detail_dir)

    @abstractmethod
    def retranlate_UI(self):
        pass

    @abstractmethod
    def run_crawler(self):
        pass
