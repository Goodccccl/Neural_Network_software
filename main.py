import sys
from PyQt5.QtWidgets import *

from home_page import Home_page


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Home_page()
    mainwindow.show()
    sys.exit(app.exec_())
