import cv2 as cv
import numpy as np

# 读取视频文件
file = 'videos/empty.mp4'
cap = cv.VideoCapture(file)
FPS = cap.get(cv.CAP_PROP_FPS)
H = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
W = cap.get(cv.CAP_PROP_FRAME_WIDTH)
print('video is loaded. {}fps, {}x{}'.format(FPS, W, H))

# 根据采样率把图片保存到ndarray
S = 4  # 原始视频中每4帧输出一张图片
success, frame = cap.read()
n_frame = 0
n_jpg = 0
while success:
    if n_frame % S == 0:
        filename = 'empty_{}.jpg'.format(n_jpg)
        cv.imwrite(filename, frame)
        # print('{} saved'.format(filename))
        n_jpg += 1
    n_frame += 1
    success, frame = cap.read()
print('{} frame got, {} jpg files saved'.format(n_frame, n_jpg))