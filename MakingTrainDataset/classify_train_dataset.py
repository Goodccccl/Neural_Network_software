import os
import shutil

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class Classify_train_dataset_page(QWidget):
    def __init__(self):
        super(Classify_train_dataset_page, self).__init__()
        loadUi('uis/classify_train_dataset.ui', self)

        self.initUi()

    def initUi(self):
        self.toolButton_select_inputdata_dir.clicked.connect(self.select_classify_inputdata_dir)  # 选择数据文件夹
        self.pushButton_creat_classify_dataset.clicked.connect(self.start_generating_classify_dataset)  # 生成分类数据集
        self.pushButton_next.clicked.connect(self.jump2classify)  # 跳转到分类功能界面

    def select_classify_inputdata_dir(self):
        self.inputdata_dir = QtWidgets.QFileDialog.getExistingDirectory(None, '请选择数据所处文件夹', 'C:/')
        self.classify_inputdata_path.setText(self.inputdata_dir)

    def start_generating_classify_dataset(self):
        if self.classify_inputdata_path.text() == '':
            QMessageBox.warning(self, "警告", "未选择数据文件！", QMessageBox.Ok)
        # elif self.comboBox_augment.currentIndex() == -1:
        #     QMessageBox.warning(self, "警告", "请选择是否进行数据增强后再生成数据集！", QMessageBox.Ok)

        else:
            files = os.listdir(self.inputdata_dir)
            if not files:
                QMessageBox.warning(self, "警告", "选择的文件夹为空，请重新选择后再生成数据集！", QMessageBox.Ok)
            else:
                from plugins.auto_yolov8_dataset import make_dataset_dir_classify, get_cls_classes
                self.dataset_path = os.path.join(os.path.dirname(self.inputdata_dir), 'classify_dataset')
                if os.path.exists(self.dataset_path):
                    shutil.rmtree(self.dataset_path)
                    os.mkdir(self.dataset_path)
                else:
                    os.mkdir(self.dataset_path)
                train = os.path.join(self.dataset_path, 'train')
                val = os.path.join(self.dataset_path, 'val')
                os.mkdir(train)
                os.mkdir(val)
                self.classes = get_cls_classes(self.inputdata_dir)
                self.plainTextEdit.setPlainText("开始制作数据集：\n"
                                                "train:{}\nval:{}\nclasses:{}".format(train, val, self.classes))
                QtWidgets.QApplication.processEvents()  # 刷新plainTextEdit中的显示
                make_dataset_dir_classify(self.inputdata_dir, self.dataset_path, self.classes, train_percent=0.8)
                self.plainTextEdit.appendPlainText('\n数据集制作完成，可以点击下一步。')

    def jump2classify(self):
        from function_page.classify_page import Classify_page
        mark = '下一步'
        text = self.plainTextEdit.toPlainText()  # 获取文本编辑框内容
        if mark in text:
            # 跳转前修改数据集的配置文件
            from plugins.utils import updata_cfg, updata_cfg2
            cfg_path = 'yolov8/ultralytics/yolo/data/datasets/mydata_classify.yaml'
            updata_cfg(cfg_path, 'path', self.dataset_path)
            for index_class in enumerate(self.classes):
                updata_cfg2(cfg_path, 'names', index_class[0], index_class[1])
            updata_cfg(cfg_path, 'nc', len(self.classes))
            self.classify_page = Classify_page()
            self.classify_page.show()
        else:
            QMessageBox.warning(self, "警告", "数据集未制作完毕，请制作数据集后再点击下一步。", QMessageBox.Ok)

    #TODO 数据增强待添加
