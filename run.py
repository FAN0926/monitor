# -*-coding=utf-8 -*-

"""
Author: Pinef
Email: fan0926@bupt.edu.cn
date: 2019/11/6 15:36
desc: 运行从目标检测到切割合并的一整个流程，作用于文件夹内所有以endwith结尾的文件
"""

import time
from tqdm import tqdm
import object_detection
import cut

if __name__ == '__main__':
    src_folder = r'D:\surface\screenshot\11.6_nodeal'
    endwith = '.mp4'
    for x in object_detection.get_file_list(src_folder, endwith):
        object_detection.object_detect(x)
        cut.start(src_file=x)
