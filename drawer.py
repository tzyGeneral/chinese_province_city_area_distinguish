import json
import time
from resources.config import shenToquDic, shenToshiDic


class City:
    def __init__(self):
        self.shenToshi = shenToshiDic
        self.shenToqu = shenToquDic
        self.shiToQu = None

    def readData(self):
        """
        读取市-区的数据
        :return:
        """
        with open('./resources/shiToQu.json', 'r', encoding='utf-8') as f:
            load_data = json.load(f)
        self.shiToQu = load_data

    def test(self):
        """
        测试
        :return:
        """
        if self.shiToQu is None:
            self.readData()
        l = []
        for shi in self.shiToQu:
            print(shi)
            l.append(shi)

    def get_indexes(self, _string: str, _char: str):
        """
        用来返回指定的_char在_string的全部索引
        """
        index_list = []
        index = _string.find(_char)
        if index != -1:
            index_list += [index, index + len(_char)]
        else:
            index_list = []
        return index_list

    def build_model(self, string: str):
        """
        省市区自动纠错
        :param string:
        :return:
        """
        if self.shiToQu is None:
            self.readData()

        indexkList = []
        modelList = []

        shen_search = ''
        shi_search = ''
        # 首先搜素省级别
        for shen in self.shenToshi:
            index = self.get_indexes(string, shen)
            if index != []:
                string = string.replace(shen, '*' * len(shen))
                shen_search = shen
                indexkList.append(index)
                modelList.append('省')

        # 加入没有搜素到省一级别，则遍历市级别
        if not shen_search:
            for shi in self.shiToQu:
                index_shi = self.get_indexes(string, shi)
                if index_shi != []:
                    string = string.replace(shi, '*' * len(shi))
                    shi_search = shi
                    indexkList.append(index_shi)
                    modelList.append('市')
        # 假如搜素到了省，则再该省下搜索市级别
        else:
            for shi in self.shenToshi[shen_search]:
                index_shi = self.get_indexes(string, shi)
                if index_shi != []:
                    string = string.replace(shi, '*' * len(shi))
                    shi_search = shi
                    indexkList.append(index_shi)
                    modelList.append('市')
        # 假如没有搜索到了市级别,则遍历区列表

        if not shi_search:
            # 假如搜索到了省没有搜索到市,则遍历该省下的所有区(todo)
            if shen_search:
                for qu in self.shenToqu[shen_search]:
                    index_qu = self.get_indexes(string, qu)
                    if index_qu != []:
                        string = string.replace(qu, '*' * len(qu))
                        indexkList.append(index_qu)
                        modelList.append('区')
            else:
                # 假如没有搜索到省也没有搜索到市，则遍历所有的区
                _quList = []
                for shenName in self.shenToqu:
                    _quList.extend(self.shenToqu[shenName])
                for qu in _quList:
                    index_qu = self.get_indexes(string, qu)
                    if index_qu != []:
                        string = string.replace(qu, '*' * len(qu))
                        indexkList.append(index_qu)
                        modelList.append('区')
        # 假如搜索到了市级别，则遍历改市下的区列表
        else:

            # 假如省，市都能匹配上，则按照次序查询区
            if shen_search:
                for qu in self.shiToQu[shi_search]:
                    index_qu = self.get_indexes(string, qu)
                    if index_qu != []:
                        string = string.replace(qu, '*' * len(qu))
                        indexkList.append(index_qu)
                        modelList.append('区')
            # 假如没有省，只是查询到了市，查询市条件下的区
            else:
                for qu in self.shiToQu[shi_search]:
                    index_qu = self.get_indexes(string, qu)
                    if index_qu != []:
                        string = string.replace(qu, '*' * len(qu))
                        indexkList.append(index_qu)
                        modelList.append('区')

        fayuanString = ['中级人民法院', '中级法院', '互联网法院', '第一法院', '第二法院', '高级法院', '基层法院', '高级人民法院', '海事法院', '知识产权法院', '最高人民法院',
                        '铁路运输法院', '运输中级法院', '人民法院', '农垦法院']

        for fayuan in fayuanString:
            fayuan_index = self.get_indexes(string, fayuan)
            if fayuan_index != []:
                indexkList.append(fayuan_index)
                modelList.append(fayuan)
                break
        else:
            print(string)
        model = dict(zip(modelList, indexkList))
        print(model)
        return model


m = City()
m.build_model('赣州市于都县')