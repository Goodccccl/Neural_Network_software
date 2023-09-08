import os.path
import threading
import time

import pandas as pd
import yaml
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')
import PyQt5.sip as sip


class MyFigure(FigureCanvas):
    def __init__(self, width, height, dpi):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)


class Detect_page(QWidget):
    def __init__(self):
        super(Detect_page, self).__init__()
        loadUi('uis/detect.ui', self)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.step = 0

        self.initUi()

    def initUi(self):
        self.toolButton_select_saveDir.clicked.connect(self.get_save_dir)
        self.pushButton_start_train.clicked.connect(self.start_train)

    def draw_curve_function(self, epochs, precisions, recalls):
        # 具体曲线函数
        self.F = MyFigure(width=3, height=2, dpi=100)

        from pylab import mpl
        mpl.rcParams["font.sans-serif"] = ["SimHei"]
        mpl.rcParams["axes.unicode_minus"] = False  # 解决中文不显示问题

        self.F.ax.plot(epochs, precisions, 'r', epochs, recalls, 'b')
        self.F.ax.legend(labels=["precision", "recall"])
        self.F.ax.set_xlabel("epochs")
        self.F.ax.set_ylabel("precision/recall")
        self.F.ax.set_title("准确率/召回率曲线")
        if self.verticalLayout_1.count() < 2:
            self.verticalLayout_1.addWidget(self.F)

    def draw_curve(self):
        # 绘制曲线
        global sign
        csv_path = os.path.join(self.save_dir, 'results.csv')
        while not os.path.exists(csv_path):
            time.sleep(1)
        epochs_num = int(self.lineEdit_epochs.text())
        epochs = []
        precisions = []
        recalls = []
        i = 0
        while i < epochs_num:
            # print("while大循环， 此时i={}".format(i))
            csv_data = pd.read_csv(csv_path, header=None)
            now_epoch = len((csv_data.iloc[1:, 0].tolist()))
            # print("now_epoch={}".format(now_epoch))
            if i < now_epoch:
                # print("此时i小于now_epoch,画图操作")
                self.step += 1
                data = csv_data.iloc[i + 1, :]
                epoch = int(data[0])
                precision = float(data[4])
                recall = float(data[5])
                epochs.append(epoch + 1)
                precisions.append(precision)
                recalls.append(recall)
                if self.step == 1:
                    self.draw_curve_function(epochs, precisions, recalls)
                    self.plainTextEdit.appendPlainText(
                        "Epoch:{}/{}  box_loss:{}  cls_loss:{}  dfl_loss:{}  precision:{}  recall:{}  "
                        "mAP50:{}  mAP50-95:{}\n".format(int(data[0]) + 1, int(epochs_num), float(data[1]),
                                                         float(data[2]), float(data[3]), float(data[4]), float(data[5]),
                                                         float(data[6]), float(data[7])))
                    QtWidgets.QApplication.processEvents()
                    i += 1
                    time.sleep(1)
                else:
                    sip.delete(self.F)
                    self.draw_curve_function(epochs, precisions, recalls)
                    self.plainTextEdit.appendPlainText(
                        "Epoch:{}/{}  box_loss:{}  cls_loss:{}  dfl_loss:{}  precision:{}  recall:{}  "
                        "mAP50:{}  mAP50-95:{}\n".format(int(data[0]) + 1, int(epochs_num), float(data[1]),
                                                         float(data[2]), float(data[3]), float(data[4]), float(data[5]),
                                                         float(data[6]), float(data[7])))
                    QtWidgets.QApplication.processEvents()
                    i += 1
                    time.sleep(1)
            else:   #TODO 解决训练未达到epochs就停止训练时不退出绘图循环的bug
                if i == epochs_num:
                    break
                else:
                    end_sign = os.path.join(self.save_dir, 'result.png')
                    if not os.path.exists(end_sign):
                        time.sleep(1)
                    else:
                        break

    def get_save_dir(self):
        self.save_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择保存地址", "C:/")
        self.lineEdit_save_dir.setText(self.save_dir)

    def start_train(self):
        if self.lineEdit_epochs.text() == '':
            QMessageBox.warning(self, "警告", "未填写epochs。", QMessageBox.Ok)
        elif self.lineEdit_batch.text() == '':
            QMessageBox.warning(self, "警告", "未填写batch。", QMessageBox.Ok)
        elif self.lineEdit_imgsz.text() == '':
            QMessageBox.warning(self, "警告", "未填写imgsz。", QMessageBox.Ok)
        elif self.lineEdit_save_dir.text() == '':
            QMessageBox.warning(self, "警告", "未选择保存地址。", QMessageBox.Ok)
        else:
            # 修改配置参数
            cfg_path = "yolov8/ultralytics/yolo/cfg/default.yaml"
            task = 'detect'
            mode = 'train'
            model = os.path.join('yolov8/weights', self.comboBox_model.currentText() + '.pt')
            epochs = int(self.lineEdit_epochs.text())
            batch = int(self.lineEdit_batch.text())
            imgsz = int(self.lineEdit_imgsz.text())
            save_dir = self.save_dir
            from plugins.utils import read_cfg
            time.sleep(1)
            cfg_data = read_cfg(cfg_path)
            cfg_data['task'] = task
            cfg_data['mode'] = mode
            cfg_data['model'] = model
            cfg_data['epochs'] = epochs
            cfg_data['imgsz'] = imgsz
            cfg_data['batch'] = batch
            cfg_data['save_dir'] = save_dir
            with open(cfg_path, 'w', encoding='utf-8') as f:
                yaml.dump(cfg_data, f, sort_keys=False)
            self.plainTextEdit.setPlainText("配置文件修改完毕，开始训练...")
            QtWidgets.QApplication.processEvents()
            # 调用训练
            from yolov8.ultralytics.yolo.v8.detect import train
            train_curve = threading.Thread(target=train)
            train_curve.start()
            self.draw_curve()
            # train_curve.join()
            self.plainTextEdit.appendPlainText("训练结束，训练结果保存在{}".format(save_dir))
            QtWidgets.QApplication.processEvents()
