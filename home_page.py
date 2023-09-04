from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from MakingTrainDataset.classify_train_dataset import Classify_train_dataset_page
from MakingTrainDataset.detect_train_dataset import  Detect_train_dataset_page
from MakingTrainDataset.segment_train_dataset import Segment_train_dataset_page
from MakingTrainDataset.abnormal_train_dataset import Abnormal_train_dataset_page


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
        # 打开分类确定数据界面
        self.classify_page = Classify_train_dataset_page()
        self.classify_page.show()

    def open_detect(self):
        # 打开目标检测确定数据界面
        self.detect_page = Detect_train_dataset_page()
        self.detect_page.show()

    def open_segment(self):
        # 打开分割确定数据界面
        self.segment_page = Segment_train_dataset_page()
        self.segment_page.show()

    def open_abnormal(self):
        # 打开异常检测确定数据界面
        self.abnoraml_page = Abnormal_train_dataset_page()
        self.abnoraml_page.show()