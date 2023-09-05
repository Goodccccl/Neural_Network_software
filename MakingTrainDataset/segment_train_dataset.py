import os
import shutil

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

class Segment_train_dataset_page(QWidget):
    def __init__(self):
        super(Segment_train_dataset_page, self).__init__()
        loadUi('uis/segment_train_dataset.ui', self)

        self.initUi()

    def initUi(self):
        self.toolButton_select_inputdata_dir.clicked.connect(self.select_segment_inputdata_dir)  # 选择数据文件夹
        self.pushButton_creat_segment_dataset.clicked.connect(self.start_generating_segment_dataset)  # 生成分类数据集
        self.pushButton_next.clicked.connect(self.jump2segment)  # 跳转到分类功能界面

    def select_segment_inputdata_dir(self):
        self.inputdata_dir = QtWidgets.QFileDialog.getExistingDirectory(None, '请选择数据所处文件夹', 'C:/')
        self.segment_inputdata_path.setText(self.inputdata_dir)

    def start_generating_segment_dataset(self):
        if self.segment_inputdata_path.text() == '':
            QMessageBox.warning(self, "警告", "未选择数据文件！", QMessageBox.Ok)
        elif self.comboBox_augment.currentIndex() == -1:
            QMessageBox.warning(self, "警告", "请选择是否进行数据增强后再生成数据集！", QMessageBox.Ok)

        else:
            files = os.listdir(self.inputdata_dir)
            if not files:
                QMessageBox.warning(self, "警告", "选择的文件夹为空，请重新选择后再生成数据集！", QMessageBox.Ok)
            else:
                from plugins.auto_yolov8_dataset import make_dataset_dir_seg, make_mydata_segment
                self.dataset_path = os.path.join(os.path.dirname(self.inputdata_dir), 'segment_dataset')
                if os.path.exists(self.dataset_path):
                    shutil.rmtree(self.dataset_path)
                    make_dataset_dir_seg(self.dataset_path)   # 制作数据集放置文件夹
                else:
                    make_dataset_dir_seg(self.dataset_path)
                self.plainTextEdit.setPlainText("开始制作数据集：{}".format(self.dataset_path))
                QtWidgets.QApplication.processEvents()  # 刷新plainTextEdit中的显示

                from plugins.utils import get_classes, get_shapeType, get_suffix
                self.classes = get_classes(self.inputdata_dir)
                suffix = get_suffix(self.inputdata_dir)
                shape_type = get_shapeType(self.inputdata_dir)
                if self.comboBox_augment.currentText() == 'True':
                    if self.lineEdit_augmentNb.text() == '':
                        QMessageBox.warning(self, "警告", "选择数据增强后需要填写增强次数。",QMessageBox.Ok)
                    else:
                        aug_times = int(self.lineEdit_augmentNb.text())
                        from plugins.auto_yolov8_dataset import Augment_json
                        Augment_json(self.inputdata_dir, aug_times, suffix)
                        augmented_dir = os.path.join(os.path.dirname(self.inputdata_dir), 'augmented')  # 获取数据增强后的文件夹地址
                        self.plainTextEdit.appendPlainText('\n数据集增强完成，存放在{}\n开始制作数据集:'.format(augmented_dir))
                        QtWidgets.QApplication.processEvents()
                        make_mydata_segment('segment', augmented_dir, self.dataset_path, self.classes, shape_type, suffix)
                        self.plainTextEdit.appendPlainText('\n数据集制作完成，可以点击下一步。')
                        QtWidgets.QApplication.processEvents()
                else:
                    make_mydata_segment('segment', self.inputdata_dir, self.dataset_path, self.classes, shape_type, suffix)
                    self.plainTextEdit.appendPlainText('\n数据集制作完成（未进行数据增强），可以点击下一步。')
                    QtWidgets.QApplication.processEvents()

    def jump2segment(self):
        from function_page.segment_page import Segment_page
        mark = '下一步'
        text = self.plainTextEdit.toPlainText()  # 获取文本编辑框内容
        if mark in text:
            # 跳转前修改数据集的配置文件
            from plugins.utils import updata_cfg, updata_cfg2
            cfg_path = 'yolov8/ultralytics/yolo/data/datasets/mydata_seg.yaml'
            updata_cfg(cfg_path, 'path', self.dataset_path)
            for index_class in enumerate(self.classes):
                updata_cfg2(cfg_path, 'names', index_class[0], index_class[1])
            self.segment_page = Segment_page()
            self.segment_page.show()
        else:
            QMessageBox.warning(self, "警告", "数据集未制作完毕，请制作数据集后再点击下一步。", QMessageBox.Ok)