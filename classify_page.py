from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Classify_page(QWidget):
    def __init__(self):
        super(Classify_page, self).__init__()
        loadUi('uis/classify.ui', self)
