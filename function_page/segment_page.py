from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Segment_page(QWidget):
    def __init__(self):
        super(Segment_page, self).__init__()
        loadUi('uis/segment.ui', self)