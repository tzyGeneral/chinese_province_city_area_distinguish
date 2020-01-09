# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree
import time
import random


class Statistics:
    def __init__(self):
        self.baseUrl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
        self.url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'
        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
            'Referer': 'https://www.toutiao.com'
        }
        self.shenToShiDic = {}
        self.shenToQuDic = {}
        self.shiToQuDic = {}
        self.checkList = []

    def getHtml(self, url):
        """
        请求一个url获取响应内容
        :param url:
        :return:
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = "gbk"
            if response.status_code != 200:
                self.getHtml(url)
            return response.text
        except Exception as e:
            print(e)
            time.sleep(random.randint(1, 3))
            self.getHtml(url)

    def parse(self, html, xpathStr):
        """
        解析页面函数
        :param html:
        :param xpathStr:
        :return:
        """
        page = etree.HTML(html)
        data = page.xpath(xpathStr)
        return data

    def saveData2File(self, data, fileName):
        """
        保存进json文件
        :return:
        """
        with open(fileName, 'w', encoding='utf-8') as f:
            json_str = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(json_str)

    def getShenToShi(self):
        """
        获取 省-市 的字典
        :return:
        """
        shenData = self.getHtml(self.url)
        shenData = self.parse(html=shenData, xpathStr="//tr[@class='provincetr']//td//a")
        for shen in shenData:
            shenName = shen.text
            shiUrl = self.baseUrl + (shen.values())[0]
            shiData = self.getHtml(shiUrl)
            shiName = self.parse(html=shiData, xpathStr="//tr//tr//tr//td[2]//a")
            shiNameList = [x.text for x in shiName]
            self.shenToShiDic[shenName] = shiNameList

    def getShenToQu(self):
        """
        获取 省-区 的字典
        :return:
        """
        shenData = self.getHtml(self.url)
        shenData = self.parse(html=shenData, xpathStr="//tr[@class='provincetr']//td//a")
        for shen in shenData:
            shenName = shen.text
            shiUrl = self.baseUrl + (shen.values())[0]
            shiData = self.getHtml(shiUrl)
            # 获取每个市级的url
            qu = []
            shiUrl = self.parse(html=shiData, xpathStr="//tr//tr//tr//td[2]//a/@href")
            for shiurl in shiUrl:
                quUrl = self.baseUrl + shiurl
                quHtml = self.getHtml(quUrl)
                quNameList = self.parse(html=quHtml, xpathStr="//tr//td[2]//a[1]")
                print(quNameList)
                quNameList = [x.text for x in quNameList]
                if quNameList == []:
                    self.checkList.append([shenName,quUrl])
                qu.extend(quNameList)
            self.shenToQuDic[shenName] = qu
        print(self.shenToQuDic)
        print(self.checkList)

    def getShiToQu(self):
        """
        获取 市-区的字典
        :return:
        """
        shenData = self.getHtml(self.url)
        shenData = self.parse(html=shenData, xpathStr="//tr[@class='provincetr']//td//a")
        for shen in shenData:
            shenName = shen.text
            print(shenName)
            shiUrl = self.baseUrl + (shen.values())[0]
            shiData = self.getHtml(shiUrl)
            # 获取每个市级的url
            shiUrlAndName = self.parse(html=shiData, xpathStr="//tr//tr//tr//td[2]//a")
            if shiUrlAndName == []:
                print('=====')
                print(shiUrl, shenName)
                continue
            for shi in shiUrlAndName:
                shiName = shi.text
                if shiName == '市辖区':
                    shiName = shenName
                quUrl = self.baseUrl + (shi.values())[0]
                quHtml = self.getHtml(quUrl)
                quNameList = self.parse(html=quHtml, xpathStr="//tr//td[2]//a[1]")
                quNameList = [x.text for x in quNameList]
                if quNameList == []:
                    self.checkList.append([shenName, quUrl, shiName])
                print(quNameList)
                self.shiToQuDic[shiName] = quNameList
        print(self.checkList)
        self.saveData2File(self.shiToQuDic, 'shiToQu_new.json')

    def getLostCheck(self):
        lastList = [['山西省', 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/14/1402.html', '大同市'], ['安徽省', 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/34/3405.html', '马鞍山市'], ['西藏自治区', 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/54/5425.html', '阿里地区'], ['新疆维吾尔自治区', 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/65/6528.html', '巴音郭楞蒙古自治州']]
        for shen, quUrl,shji in lastList:
            quHtml = self.getHtml(quUrl)
            quNameList = self.parse(html=quHtml, xpathStr="//tr//td[2]//a[1]")
            quNameList = [x.text for x in quNameList]
            print(shji, quNameList)


if __name__ == "__main__":
    m = Statistics()
    m.getLostCheck()


