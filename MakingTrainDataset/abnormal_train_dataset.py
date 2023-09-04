from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Abnormal_train_dataset_page(QWidget):
    def __init__(self):
        super(Abnormal_train_dataset_page, self).__init__()
        loadUi('uis/abnormal_train_dataset.ui', self)

