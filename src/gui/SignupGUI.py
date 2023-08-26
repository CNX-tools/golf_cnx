import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from src.gui.BaseGUI import BaseGUI


class SignupGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super(SignupGUI, self).__init__(MainWindow)

        self.sign_up_radioButton.setChecked(True)
