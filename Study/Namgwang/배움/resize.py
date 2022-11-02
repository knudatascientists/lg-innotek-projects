import pandas as pd 
import numpy as np
import cv2
path = r"C:\Users\USER\Documents\GitHub\python_exer\221027\Lenna.png"
img = cv2.imread(path)
lena_nearest = cv2.resize(img, dsize=(1000,1000), interpolation=cv2.INTER_NEAREST)
lena_cubic = cv2.resize(img, dsize=(1000,1000), interpolation=cv2.INTER_CUBIC)

cv2.imshow("nearest", lena_nearest)
cv2.imshow("cubic", lena_cubic)
cv2.waitKey(0)