import traceback
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget
import sys
import os

from src.gui.SigninGUI import SiginGUI


def add_path_to_env():
    # Add PyQt5 path to environment
    new_path = os.path.join(os.getcwd(), '.venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms')
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = new_path


if __name__ == "__main__":
    add_path_to_env()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    try:
        app = QApplication(sys.argv)
        main_window = QStackedWidget()

        sign_in_gui = SiginGUI(main_window)
        main_window.addWidget(sign_in_gui)

        # Set the main window size
        main_window.setFixedHeight(650)
        main_window.setFixedWidth(1130)
        main_window.setWindowTitle("Golf Booking by @DM2uan")
        main_window.setCurrentIndex(0)
        main_window.setWindowIcon(QIcon('./assets/logo.jpg'))
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_message = f"An error occurred:\n{traceback.format_exc()}"
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)
