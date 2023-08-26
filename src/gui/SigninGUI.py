import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from src.gui.BaseGUI import BaseGUI


class SiginGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super(SiginGUI, self).__init__(MainWindow)
