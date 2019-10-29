# -*-coding=utf-8 -*-

"""
Author: Pinef
Email: fan0926@bupt.edu.cn
date: 2019/10/22 17:06
desc: 
"""

import time
import datetime
from tqdm import tqdm
import subprocess
import os
import time_analysis


def cut_video(start_time, during_time, input, output):
    '''
    构造ffmpeg的切割语句，利用subprocess运行cmd语句
    :param start_time:
    :param during_time:
    :param input:
    :param output:
    :return:
    值得注意的是，ffmpeg 为了加速，会使用关键帧技术， 所以有时剪切出来的结果在起止时间上未必准确。
    通常来说，把 -ss 选项放在 -i 之前，会使用关键帧技术； 把 -ss 选项放在 -i 之后，则不使用关键帧技术。
    '''
    cmd = [
        'ffmpeg',
        '-ss',
        start_time,
        '-t',
        during_time,
        '-accurate_seek',
        '-i',
        input,
        '-c',
        'copy',
        '-copyts',
        output]
    subprocess.call(cmd)


def concat_video(filelistpath, output):
    '''
    构造ffmpeg的合并连接语句，利用subprocess运行cmd语句
    :param filelistpath:
    :param output:
    :return:
    '''
    cmd = [
        'ffmpeg',
        '-f',
        'concat',
        '-safe',
        '0',
        '-i',
        filelistpath,
        '-c',
        'copy',
        output]
    subprocess.call(cmd)


def start(src_folder, endwith, blankspacetime):
    '''
    对文件夹内的所有视频文件进行分析，并根据分析结果进行剪辑合并
    :param src_folder:
    :param endwith:
    :param blankspacetime: 允许的空白时间
    :return:
    '''
    src_paths = [os.path.join(src_folder, path) for path in os.listdir(src_folder) if path.endswith(endwith)]
    print('src_paths:', src_paths)
    for i in tqdm(src_paths):  # 开始对每个文件夹下的每个视频文件进行剪辑
        txt_path = i.replace(endwith, '.txt')  # 读取该文件对应的时间文件
        out_file_list = []                    # 切割后的视频文件路径
        if os.path.exists(txt_path):
            get_time_list = time_analysis.analysis(txt_path, blankspacetime)       # 对时间文件进行分析，找到出现移动目标的时间段，
            # print(get_time_list)
            for a in range(int(len(get_time_list) / 2)):   # 根据时间段对视频进行剪切
                start_time = get_time_list.pop(0)
                #增加切割片段前的冗余
                if start_time != '0:00:00' and start_time != '0:00:01' and start_time != '0:00:02':
                    start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
                    start_time = start_time - datetime.timedelta(seconds=1)    # 增加1s的冗余
                    start_time = start_time.strftime('%H:%M:%S')
                # print('修改后的时间为：', start_time)
                new_start_time = "Sat Mar 28 {} 2019".format(start_time)
                end_time = "Sat Mar 28 {} 2019".format(get_time_list.pop(0))
                strftime1 = time.mktime(time.strptime(new_start_time, "%a %b %d %H:%M:%S %Y"))  # 格式化为时间戳
                strftime2 = time.mktime(time.strptime(end_time, "%a %b %d %H:%M:%S %Y"))
                during_time = str(int(strftime2 - strftime1))
                cut_video(start_time, during_time, i, i.replace(endwith, '_{}'.format(a)+endwith))  # 对该段进行剪辑
                out_file_list.append(i.replace(endwith, '_{}'.format(a)+endwith))

            with open('fileline.txt', 'w+', encoding='utf-8') as f:
                for file in out_file_list:
                    f.write("file '{}'".format(file))
                    f.write('\n')
            concat_video('fileline.txt', txt_path.replace('.txt', '_fin'+endwith))
            for list in out_file_list:
                if os.path.exists(list):
                    os.remove(list)

        else:
            print("txt_path:", txt_path, '不存在，请检查。')
            continue


if __name__ == '__main__':
    start(r'D:\surface\no_deal', '.mp4', 5)
    # start(r'D:\surface\screenshot', '.mp4', 3)
    # start(os.getcwd(), '.mp4', 3)