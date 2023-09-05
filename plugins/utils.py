import json
import os.path
import random
import shutil

import pandas as pd
import yaml
from matplotlib import pyplot as plt


def get_shapeType(src_inputdata_dir):
    # 获取json文件中标注的格式
    jsons_path = os.path.join(src_inputdata_dir, 'json')
    jsons = os.listdir(jsons_path)
    json_ = jsons[0]
    json_path = os.path.join(jsons_path, json_)
    data = json.load(open(json_path, 'r', encoding='gb2312', errors='ignore'))
    shape = data['shapes'][0]
    shapeType = shape['shape_type']
    return shapeType

def get_suffix(src_inputdata_dir):
    images = os.listdir(src_inputdata_dir)
    if images[0] == 'json':
        suffix = images[1].split('.')[-1]
        return suffix
    else:
        suffix = images[0].split('.')[-1]
        return suffix

def get_classes(src_inputdata_dir):
    # 获取json文件中标注的类别
    jsons_path = os.path.join(src_inputdata_dir, 'json')
    jsons = os.listdir(jsons_path)
    classes = []
    for json_ in jsons:
        json_path = os.path.join(jsons_path, json_.replace('\n', ''))
        data = json.load(open(json_path, 'r', encoding='gb2312', errors='ignore'))
        for i in data['shapes']:
            label_name = i['label']
            if label_name not in classes:
                classes.append(label_name)
    return classes


def read_cfg(cfg_path):
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        return None


def updata_cfg(cfg_path, key, val):
    # 更新单层键值对的配置文件
    cfg_data = read_cfg(cfg_path)
    cfg_data[key] = val
    with open(cfg_path, 'w', encoding='utf-8') as f:
        yaml.dump(cfg_data, f, sort_keys=False)


def updata_cfg2(cfg_path, key1, key2, v):
    # 更新多层键值对的配置文件
    cfg_data = read_cfg(cfg_path)
    if key2 == 0:
        cfg_data[key1] = {}
        cfg_data[key1][key2] = v
        with open(cfg_path, "w", encoding='utf-8') as f:
            yaml.dump(cfg_data, f, sort_keys=False)
    else:
        cfg_data[key1][key2] = v
        with open(cfg_path, "w", encoding='utf-8') as f:
            yaml.dump(cfg_data, f, sort_keys=False)


def draw_curve(csv_path):
    # 绘制训练曲线
    csv_data = pd.read_csv(csv_path, header=None)
    # print(csv_data)
    precisions = []
    recalls = []
    epochs = []
    epochs_num = len((csv_data.iloc[1:, 0].tolist()))
    for i in range(epochs_num):
        epoch = int(csv_data.iloc[i+1, 0])
        # print(epoch)
        precision = float(csv_data.iloc[i+1, 4])
        # print(precision)
        recall = float(csv_data.iloc[i+1, 5])
        # print(recall)
        epochs.append(epoch)
        precisions.append(precision)
        recalls.append(recall)
        plt.title("123")
        plt.xlabel("epochs")
        plt.ylabel("precisions&recalls")
        plt.plot(epochs, precisions, 'r', epochs, recalls, 'b')
        plt.legend(labels=["precision", "recall"])
        save_path = r'F:\software_try\123.jpg'
        plt.savefig(save_path)
        # plt.show(block=False)
        # plt.pause(1)
        # plt.close()