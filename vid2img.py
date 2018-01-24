import cv2 as cv
import numpy as np
import os

# 读取视频文件
f = 'videos/scissor2.mp4'
cap = cv.VideoCapture(f)
FPS = cap.get(cv.CAP_PROP_FPS)
H = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
W = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
print('video is loaded. {}fps, {}x{}'.format(FPS, W, H))

# configurations
S = 4  # 原始视频中每4帧输出一张图片
# SEED = 42  # np.random随机种子
TEST_SPLIT = 0.2

# 根据采样率把图片保存到ndarray
n_frame = 0
n_img = 0
imgs = []
success, frame = cap.read()
while success:
    if n_frame & 4 == 0:
        imgs.append(frame)
        n_img += 1
    n_frame += 1
    success, frame = cap.read()
imgs = np.asarray(imgs)
print('imgs.shape: {}'.format(imgs.shape))

# 随机打乱imgs，拆分成train和test
np.random.seed()
np.random.shuffle(imgs)
n_sample = imgs.shape[0]
n_test = int(n_sample * TEST_SPLIT)  # 向下取整
n_train = n_sample - n_test
test_set = imgs[:n_test]
train_set = imgs[n_test:]
print('train: {}, test: {}'.format(n_train, n_test))

# 设置路径，创建文件夹
base_dir = './imgs'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')
category = 'scissor'
train_category_dir = os.path.join(train_dir, category)
test_category_dir = os.path.join(test_dir, category)
if not os.path.exists(train_category_dir):
    os.makedirs(train_category_dir)
if not os.path.exists(test_category_dir):
    os.makedirs(test_category_dir)

# 保存成jpg文件
for i in range(n_test):
    filepath = os.path.join(test_category_dir, '{}_{}.jpg'.format('scissor2', i))
    cv.imwrite(filepath,test_set[i])
for i in range(n_train):
    filepath = os.path.join(train_category_dir, '{}_{}.jpg'.format('scissor2', i))
    cv.imwrite(filepath, train_set[i])

print('Done')