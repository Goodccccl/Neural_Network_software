import os
import shutil

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from plugins.utils import *

class Classify_train_dataset_page(QWidget):
    def __init__(self):
        super(Classify_train_dataset_page, self).__init__()
        loadUi('uis/classify_train_dataset.ui', self)

        self.initUi()

    def initUi(self):
        self.toolButton_select_inputdata_dir.clicked.connect(self.select_classsify_inputdata_dir)
        self.pushButton_creat_classify_dataset.clicked.connect(self.select_classify_inputdata_suffix)
        self.pushButton_creat_classify_dataset.clicked.connect(self.start_generating_classify_dataset)

    def select_classsify_inputdata_dir(self):
        self.inputdata_dir = QtWidgets.QFileDialog.getExistingDirectory(None, '请选择数据所处文件夹', 'C:/')
        self.classify_inputdata_path.setText(self.inputdata_dir)

    def select_classify_inputdata_suffix(self):
        self.inputdata_suffix = self.comboBox_suffix.currentText()

    def start_generating_classify_dataset(self):
        if self.classify_inputdata_path.text() == '':
            QMessageBox.warning(self, "警告", "未选择数据文件！", QMessageBox.Ok)
        elif self.comboBox_suffix.currentIndex() == -1:
            QMessageBox.warning(self, "警告", "请选择图片的后缀名后再生成数据集！", QMessageBox.Ok)
        elif self.comboBox_augment.currentIndex() == -1:
            QMessageBox.warning(self, "警告", "请选择是否进行数据增强后再生成数据集！", QMessageBox.Ok)

        else:
            files = os.listdir(self.inputdata_dir)
            if not files:
                QMessageBox.warning(self, "警告", "选择的文件夹为空，请重新选择后再生成数据集！", QMessageBox.Ok)
            else:
                from plugins.auto_yolov8_dataset import make_dataset_dir_classify
                dataset_path = os.path.join(os.path.dirname(self.inputdata_dir), 'classify_dataset')
                if os.path.exists(dataset_path):
                    shutil.rmtree(dataset_path)
                    os.mkdir(dataset_path)
                else:
                    os.mkdir(dataset_path)
                train = os.path.join(dataset_path, 'train')
                val = os.path.join(dataset_path, 'val')
                os.mkdir(train)
                os.mkdir(val)
                self.plainTextEdit.setPlainText("开始制作数据集：\n"
                                           "train:{}\nval:{}".format(train, val))
                QtWidgets.QApplication.processEvents()  # 刷新plainTextEdit中的显示
                make_dataset_dir_classify(self.inputdata_dir, dataset_path, train_percent=0.8)
                self.plainTextEdit.appendPlainText('\n数据集制作完成，可以点击下一步。')

