from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Detect_train_dataset_page(QWidget):
    def __init__(self):
        super(Detect_train_dataset_page, self).__init__()
        loadUi('uis/detect_train_dataset.ui', self)

