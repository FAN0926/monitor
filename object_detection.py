# -*-coding=utf-8 -*-

"""
Author: Pinef
Email: fan0926@bupt.edu.cn
date: 2019/9/23 18:23
desc:实现了物体探测类的封装，能够读取视频数据并检测每帧是否有移动物体，将结果输出保存在txt文件中
调用方法：object_detect(视频文件路径)
"""

import cv2
import numpy as np
import datetime
import time
import shutil
import traceback
import os
import tqdm

class object_detect():
    def __init__(self,video_path):
        if not os.path.exists(video_path):
            print("文件不存在，请检查")
            os._exit(1)
        self.video = video_path
        self.save_name = video_path.split('\\')[-1].split('.')[0] + '.txt'
        with open(self.save_name, 'w+', encoding='utf-8') as f:
            f.write('time flag')
            f.write('\n')
        self.detect_video(self.video)
        if self.video.rsplit('\\', 1)[0] != self.video:
            self.move_file(os.getcwd(), self.video.rsplit('\\', 1)[0], self.save_name)

    def detect_video(self, video):
        """
        retval = cv.createBackgroundSubtractorMOG2( [, history[, varThreshold[, detectShadows]]] )
        Parameters
            history Length of the history.
            varThreshold    Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.
            detectShadows   If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.
        url: https://docs.opencv.org/3.4.2/de/de1/group__video__motion.html#ga2beb2dee7a073809ccec60f145b6b29c
        """
        # MOG背景分割器
        mog = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        # 检测阴影的参数设为False能够稍微加快速度快几s，KNN要慢十几s，效果无明显差异

        camera = cv2.VideoCapture(video)
        fps = camera.get(cv2.CAP_PROP_FPS)
        ret, frame = camera.read()
        last_time = ''
        writetimeflag = True
        persecondtype = []
        pbar = tqdm.tqdm(total=camera.get(7), unit='frame')
        pbar.set_description('In this video : %s' % video)
        # print('camera total:', camera.get(7))
        while ret:
            # 为了提高速度而不进行逐帧检测，而是选择了每一秒测一帧
            if camera.get(1) % int(2) != 0:
                # print(camera.get(1))
                pbar.update(1)
                ret, frame = camera.read()  # 读取视频帧数据
                continue
            # print(str(camera.get(1) / camera.get(7)*100) + '%')
            fgmask = mog.apply(frame)
            th = cv2.threshold(np.copy(fgmask), 244, 255, cv2.THRESH_BINARY)[1]

            th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
            dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)

            image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            time_now = str(datetime.timedelta(seconds=int(camera.get(0) / 1000))).split('.')[0]
            if last_time != time_now:
                writetimeflag = True
                if len(persecondtype) != 0:
                    # print(persecondtype)
                    if 1 in persecondtype:
                        self.write_time(self.video, str(last_time), 1)
                    else:
                        self.write_time(self.video, str(last_time), 0)
                persecondtype.clear()
            for c in contours:
                if cv2.contourArea(c) > 500:   # 设定检测区域的阈值大小，小于多少不画框
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    if writetimeflag is True:
                        # self.write_time(self.video, str(time_now), 1)
                        persecondtype.append(1)
                        writetimeflag = False
            if writetimeflag is True:
                persecondtype.append(0)
                #self.write_time(self.video, str(time_now), 0)

            last_time = time_now
            pbar.update(1)

            # cv2.imshow("mog", fgmask)
            # cv2.imshow("thresh", th)
            # cv2.imshow("diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
            # cv2.imshow("detection", frame)
            ret, frame = camera.read()  # 读取视频帧数据
            if cv2.waitKey(100) & 0xff == ord("q"):
                break

        camera.release()
        pbar.close()
        cv2.destroyAllWindows()

    def write_time(self, video, time, detect):  # detect=1 means something is moving in this frame
        with open(video.split('\\')[-1].split('.')[0]+'.txt', 'a+', encoding='utf-8') as f:
            f.write(str(time)+' '+str(detect))
            f.write('\n')

    def move_file(self, src_path, dst_path, file):
        print('from : ', src_path)
        print('to : ', dst_path)
        try:
            # cmd = 'chmod -R +x ' + src_path
            # os.popen(cmd)
            f_src = os.path.join(src_path, file)
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            f_dst = os.path.join(dst_path, file)
            shutil.move(f_src, f_dst)
        except Exception as e:
            print('move_file ERROR: ', e)
            traceback.print_exc()


def get_file_list(src_folder, endwith):
        src_paths = [os.path.join(src_folder, path) for path in os.listdir(src_folder) if path.endswith(endwith)]
        print(src_paths)
        if input("按q结束，继续按其他任意键") == 'q':
            os._exit(1)
        return src_paths


if __name__ == '__main__':
    # video = r"F:\YSHS\115\VID_20190920_222525.mp4_20190923_181347.mkv"
    # video = r'F:\YSHS\A ISVID_20191012_191644_1.mp4'
    # starttime = datetime.datetime.now()
    # print(starttime)
    # video = r'test.mp4'
    # object_detect(video)
    # print(datetime.datetime.now(), '\nduring time:',datetime.datetime.now()-starttime)
    src_folder = r'F:\YSHS\test'
    endwith = '.mp4'
    for x in get_file_list(src_folder, endwith):
        object_detect(x)
        #print(x)
    # src_folder = r'D:\surface\screenshot'
    # for x in tqdm(get_file_list(src_folder,endwith)):
    #     object_detect(x)
    #     #print(x)