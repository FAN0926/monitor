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


if __name__ == '__main__':
    papa = pd.read_csv(r'F:\OneDrive - bupt.edu.cn\PycharmProjects\python_foundation\Opencv\result\test.txt', sep='\t',
                       delimiter='\s+')  # 加载papa.txt,指定它的分隔符是 \t
    papa.head()  # 显示数据的前几行
    rowNum = papa.shape[0]  # 不包括表头
    colNum = papa.columns.size
    #profile = pandas_profiling.ProfileReport(papa)
    #profile.to_file("outputfile.html")
    print(papa,rowNum,colNum)
    plt.plot(papa.time, papa.flag, 'ro-', color='#4169E1', alpha=0.8, label='一些数字')
    plt.xticks(papa.time, papa.time, rotation=90)  # 这里是调节横坐标的倾斜度，rotation是度数
    # 显示标签，如果不加这句，即使加了label='一些数字'的参数，最终还是不会显示标签
    plt.legend(loc="upper right")
    plt.xlabel('time')
    plt.ylabel('flag')

    plt.show()