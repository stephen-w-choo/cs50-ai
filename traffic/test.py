import cv2
import numpy as np
import os
import sys

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

dir = os.listdir(os.path.join("gtsrb", "0"))

img = cv2.imread("gtsrb/0/00000_00000.ppm")

print(img.shape)

img = cv2.resize(img, (30, 30))

print(img.shape)
