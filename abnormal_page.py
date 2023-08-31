from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Abnormal_page(QWidget):
    def __init__(self):
        super(Abnormal_page, self).__init__()
        loadUi('uis/abnormal.ui', self)