# -*-coding=utf-8 -*-

"""
Author: Pinef
Email: fan0926@bupt.edu.cn
date: 2019/10/18 16:34
desc: 
"""

import time
from tqdm import tqdm
import pandas as pd
import pandas_profiling
import matplotlib.pylab as plt
import matplotlib
import itertools


def mulsq(type,times):   # 为了消除噪声，构造连续列表
    tmp = [type] * times
    return tmp


def split_time(time_sq):   # 切割最后输出的时间列表使其成对出现
    start_time = time_sq.pop(0)
    end_time = time_sq.pop(0)
    return start_time,end_time


def analysis(vedio_txt_path, max_empty_time, Rrawpic=False):
    papa = pd.read_csv(vedio_txt_path, sep='\t',
                       delimiter='\s+')  # 加载papa.txt,指定它的分隔符是 \t
    # papa.head()  # 显示数据的前几行
    # rowNum = papa.shape[0]  # 不包括表头
    # colNum = papa.columns.size
    # profile = pandas_profiling.ProfileReport(papa)  # pandas的一个初步的自动的数据分析库
    # profile.to_file("outputfile.html")              # 调用库的输出可以保存为一个html文件
    count = {'1': [], '0': []}
    result = []
    for k, v in itertools.groupby(list(papa['flag'])):
        # print(type(k),len(list(v)),count[str(k)].get(str(len(list(v)))))
        times = len(list(v))
        count[str(k)].append(len(list(v)))
        if k == 1:
            result.extend(mulsq(k, times))
        if k == 0:
            if times <= max_empty_time:  # 设定容许的连零个数
                result.extend(mulsq(1, times))
            else:
                result.extend(mulsq(0, times))

    papa['new_flag'] = result
    get_time = []
    flag = False  # 默认一开始是没有检测到移动对象的，即数据为0
    for row in tqdm(papa.itertuples(index=True, name='Pandas')):
        # print(getattr(row, "time"), getattr(row, "new_flag"))
        tmp_time = getattr(row, "time")
        tmp_flag = getattr(row, "new_flag")
        if flag is False:  # 若处于未检测到的状态
            if tmp_flag == 1:  # 出现移动物体，添加此刻时间作为该段开始时间，并设置信号为已检测到的状态
                get_time.append(tmp_time)
                flag = True
                pass
            if tmp_flag == 0:  # 未出现移动物体，读取下一秒的数据
                pass
        if flag is True:
            if tmp_flag == 1:
                pass
            if tmp_flag == 0:
                get_time.append(tmp_time)
                flag = False
    if len(get_time) % 2 != 0:
        get_time.append(papa.iat[-1, 0])  # 如果获取到的时间不是成对成对的，添加文件的最后一行的第一列的时间
    # print(get_time)
    copy_get_time = get_time.copy()
    for i in range(int(len(get_time) / 2)):  # 切割时间使其成对出现
        # print(split_time(copy_get_time))
        pass

    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['font.family']='sans-serif'
    # plt.plot(papa.time, papa.flag, 'ro-', color='#4169E1', alpha=0.8, label='一些数字')
    # plt.xticks(papa.time, papa.time, rotation=90)  # 这里是调节横坐标的倾斜度，rotation是度数
    # # 显示标签，如果不加这句，即使加了label='一些数字'的参数，最终还是不会显示标签
    # plt.legend(loc="upper right")
    # plt.xlabel('time')
    # plt.ylabel('flag')
    #
    # plt.show()
    if Rrawpic:
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family']='sans-serif'
        plt.plot(papa.time, result, 'ro-', color='#4169E1', alpha=0.8, label='一些数字')
        plt.xticks(papa.time, papa.time, rotation=90)  # 这里是调节横坐标的倾斜度，rotation是度数
        # 显示标签，如果不加这句，即使加了label='一些数字'的参数，最终还是不会显示标签
        plt.legend(loc="upper right")
        plt.xlabel('time')
        plt.ylabel('flag')
        for i in range(int(len(get_time))):  # 切割时间使其成对出现
            #print(split_time(get_time))
            plt.plot(get_time[i], 1, 'r-o')
        plt.show()

    return get_time

if __name__ == '__main__':
    analysis(r'F:\OneDrive - bupt.edu.cn\PycharmProjects\python_foundation\Opencv\result\test.txt', 2, False)