from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from classify_page import Classify_page
from detect_page import Detect_page
from segment_page import Segment_page
from abnormal_page import Abnormal_page


class Home_page(QMainWindow):
    def __init__(self):
        super(Home_page, self).__init__()
        loadUi('uis/home_page.ui', self)
        self.initUi()

    def initUi(self):
        self.pushButton_classify.clicked.connect(self.open_classify)  # 分类任务按钮
        self.pushButton_detect.clicked.connect(self.open_detect)  # 目标检测任务按钮
        self.pushButton_segment.clicked.connect(self.open_segment)  # 分割任务按钮
        self.pushButton_abnormal.clicked.connect(self.open_abnormal)  # 异常检测按钮

    # 连接跳转界面函数
    def open_classify(self):
        # 打开分类界面
        self.classify_page = Classify_page()
        self.classify_page.show()

    def open_detect(self):
        # 打开目标检测界面
        self.detect_page = Detect_page()
        self.detect_page.show()

    def open_segment(self):
        # 打开分割界面
        self.segment_page = Segment_page()
        self.segment_page.show()

    def open_abnormal(self):
        # 打开异常检测界面
        self.abnoraml_page = Abnormal_page()
        self.abnoraml_page.show()