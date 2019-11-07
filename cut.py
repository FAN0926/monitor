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
        output,
        '-loglevel',
        'quiet']
    subprocess.check_call(cmd)
    # subprocess.call()
    # 执行命令，返回命令的结果和执行状态，0或者非0
    # subprocess.check_call()
    # 执行命令，返回结果和状态，正常为0 ，执行错误则抛出异常


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
        output,
        '-loglevel',
        'quiet']
    subprocess.check_call(cmd)


def start(src_folder=None, endwith='.mp4', blankspacetime=5, src_file=None):
    """
    对文件夹内的所有视频文件进行分析，并根据分析结果进行剪辑合并
    :param src_folder:与src_file二选一，如果两者同时填则只会对文件进行处理
    :param src_file:
    :param endwith:
    :param blankspacetime: 允许的空白时间
    :return:
    """
    src_paths = []
    if src_file is None and src_folder is None:
        print("无文件夹或者文件路径输入，请检查")
        os._exit(2)
    if src_file is not None:
        src_paths.append(src_file)
    else:
        src_paths = [os.path.join(src_folder, path) for path in os.listdir(src_folder) if
                     (path.endswith("_pre.mp4")or path.endswith(".mp4"))]
    print('src_paths:', src_paths)
    # 调试时或者单独运行时检查使用，使用run.py运行时会优先运行object_detection.py里的这一部分
    # x = input("确认按任意键继续，否则按q退出")
    # if x == 'q':
    #     os._exit(1)
    total_num = len(src_paths)
    current_num = 1
    try:
        # with tqdm(src_paths, desc='Total video', unit='video') as t:
        for i in src_paths:  # 开始对每个文件夹下的每个视频文件进行剪辑
            txt_path = i.replace(endwith, '.txt')  # 读取该文件对应的时间文件
            out_file_list = []                    # 切割后的视频文件路径
            if os.path.exists(txt_path):
                get_time_list = time_analysis.analysis(txt_path, blankspacetime)       # 对时间文件进行分析，找到出现移动目标的时间段，
                # print(get_time_list)
                with tqdm(range(int(len(get_time_list) / 2)), unit='part') as t2:
                    t2.set_description('Current video is %s , %d/%d' % (i, current_num, total_num))
                    for a in t2:   # 根据时间段对视频进行剪切
                        start_time = get_time_list.pop(0)
                        # 增加切割片段前的冗余
                        if start_time != '0:00:00' and start_time != '0:00:01' and start_time != '0:00:02':
                            start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
                            start_time = start_time - datetime.timedelta(seconds=1)    # 增加1s的冗余
                            start_time = start_time.strftime('%H:%M:%S')
                        # print('修改后的时间为：', start_time)
                        new_start_time = "Sat Mar 28 {} 2019".format(start_time)
                        # 如果不是视频结尾，则增加在片段后增加1秒钟
                        end_time = get_time_list.pop(0)
                        if len(get_time_list) != 0:
                            end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')
                            end_time = end_time + datetime.timedelta(seconds=1)  # 增加1s的冗余
                            end_time = end_time.strftime('%H:%M:%S')
                        new_end_time = "Sat Mar 28 {} 2019".format(end_time)
                        strftime1 = time.mktime(time.strptime(new_start_time, "%a %b %d %H:%M:%S %Y"))  # 格式化为时间戳
                        strftime2 = time.mktime(time.strptime(new_end_time, "%a %b %d %H:%M:%S %Y"))
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
    except KeyboardInterrupt:
        t2.close()
        raise
    t2.close()


if __name__ == '__main__':
    start(r'F:\YSHS\test')
    # start(r'D:\surface\screenshot', '.mp4', 3)
    # start(os.getcwd(), '.mp4', 3)