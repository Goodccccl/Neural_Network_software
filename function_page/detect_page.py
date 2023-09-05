from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Detect_page(QWidget):
    def __init__(self):
        super(Detect_page, self).__init__()
        loadUi('uis/detect.ui', self)