#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import ***************************************************************************
import requests     # webページ取得用
import lxml.html    # webページ取得データ取得
import urllib       # urlエンコード変換
import sys          # コマンドライン引数
import time         # wait用
import re           # 文字列分割用
#***********************************************************************************

class OneDataInfo:
    def __init__(self):
        self.time = "-1"        # 時間
        self.type = ""          # 種別(普通,快速,etc...)
        self.destination = ""   # 行先


    def is_invalid_data(self) -> bool:
        if self.time == "-1":
            return True
        else:
            return False

    def set_data(self, data_str: str):
        split_data = data_str.split()
        self.time = split_data[0]
        self.type = split_data[3]
        self.destination = split_data[len(split_data) - 1].split('：')[1]


class TrainTimeInfo():
    
    def __init__(self):
        """ コンストラクタ
        """
        self.__targeturl = "" # 検索対象URL
        self.__REQ_HEADER = {'User-Agent':
                             'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.42'}
    

    def get_time_info(self, target_url: str) -> list:
        """ 時刻情報取得
        [I] target_url 対象URL
        [O] 時刻情報
        """
        self.__targeturl = target_url
        # 個別のURL取得
        url_list = self.__get_time_detailes_url_list()
        # 全データ取得
        data_info_list : list[OneDataInfo] = []
        data_num = len(url_list)
        for cnt, one_url in enumerate(url_list):
            # 進捗表示
            sys.stdout.write("\r{}".format("解析中 : " + str(cnt+1) + "/" + str(data_num)))
            sys.stdout.flush()
            # 取得結果保持
            data_info_list.append(self.__get_one_data_info(one_url))
        print()
        # 文字列生成
        time_info_str_list = []
        for one_data in data_info_list:
            if one_data.is_invalid_data() == False:
                time_info_str_list.append(
                    one_data.time + "," + one_data.type + "," + one_data.destination + ",\n")
        return time_info_str_list


    def __get_time_detailes_url_list(self) -> list:
        """ 時間ごとのURLリスト取得
        [O] 時刻情報詳細URLリスト
        """
        # 一覧ページ取得
        while True:
            request_result = requests.get(self.__targeturl, headers=self.__REQ_HEADER)
            if(request_result.status_code != requests.codes['ok']):
                time.sleep(1)   # 1秒wait
            else:
                break
        # HTML取得
        html_root = lxml.html.fromstring(request_result.content)
        # 時刻表部分取得
        all_data_info = html_root.xpath(
            "//table[contains(@class, 'tblDiaDetail')]"\
                "//li[contains(@class, 'timeNumb')]"\
                    "//a")
        url_list = []
        # 時刻表内詳細データへのURL取得
        for one_data in all_data_info:
            urlinfo = one_data.items()
            if len(urlinfo) > 0 and urlinfo[0][0] == "href":
                url_list.append("https://transit.yahoo.co.jp/" + urlinfo[0][1])
        return url_list


    def __get_one_data_info(self, url: str) -> OneDataInfo:
        """ 1データ情報取得
        """
        # ページ情報取得
        while True:
            request_result = requests.get(
                url, headers=self.__REQ_HEADER)
            if request_result.status_code != requests.codes['ok']:
                time.sleep(1)   # 1秒wait
            else:
                break
        html_root = lxml.html.fromstring(request_result.content)
        # 列車情報取得
        train_info = html_root.xpath(
            "//p[contains(@class, 'txtTrainInfo')]")
        destination_info = html_root.xpath(
            "//div[contains(@id, 'mdDiaStopSta')]"\
            "//div[contains(@class, 'labelMedium')]"\
            "//h2[contains(@class, 'title')]")
        if len(train_info) > 0 and len(destination_info) > 0:
            # 結果用情報を生成し各要素に設定
            data_info = OneDataInfo()
            split_data = train_info[0].text_content().encode(
                'utf-8').decode('utf-8').split()
            # 時間はHH:MMの形式に合わせる
            if split_data[0][1:2] ==":":
                data_info.time = "0" + split_data[0]
            else:
                data_info.time = split_data[0]
            data_info.type = split_data[3]
            destination_split_info = destination_info[0].text_content().encode(
                'utf-8').decode('utf-8').split()
            data_info.destination = re.split(
                '→|行き', destination_split_info[1])[1]
            return data_info
        else:
            return OneDataInfo()




def main(args):
    if len(args) < 1:
        print("URLを指定してください")
        return 
    train_time_info = TrainTimeInfo()
    result_list = train_time_info.get_time_info(args[1])
    # ファイル出力
    with open('result.txt', mode='a', encoding='utf-8') as resultfile:
        resultfile.write("------------------------------------------------------------------\n")
        resultfile.writelines(result_list)
        resultfile.write("------------------------------------------------------------------\n")


if __name__ == "__main__":
    main(sys.argv)
    #tmp = ["","https://transit.yahoo.co.jp/station/time/25853/?kind=1&gid=1770&q=%E5%A4%A7%E9%98%AA&tab=time"]
    #main(tmp)
