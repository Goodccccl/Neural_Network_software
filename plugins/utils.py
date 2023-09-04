import json
import os.path
import random
import shutil


class utils:
    def __init__(self):
        self.src_inputdata_dir = None

    def get_shapeType(self):
        # 获取json文件中标注的格式
        jsons_path = os.path.join(self.src_inputdata_dir, 'json')
        jsons = os.listdir(jsons_path)
        json_ = jsons[0]
        json_path = os.path.join(jsons_path, json_)
        data = json.load(open(json_path, 'r', encoding='gb2312', errors='ignore'))
        shape = data['shape'][0]
        shapeType = shape['shape_type']
        return shapeType
