import pandas as pd 
import numpy as np
import cv2
path = r"C:\Users\USER\Documents\GitHub\python_exer\221027\Lenna.png"
img = cv2.imread(path)
(h,w) = img.shape[:2]

src_array = np.array([[0,0],[0,511],[511,0],[511,511]], np.float32)
dst_array = np.array([[100,100],[100,411],[411,200],[411,311]], np.float32)

per_mat = cv2.getPerspectiveTransform(src_array, dst_array)
lena_per = cv2.warpPerspective(img, per_mat, (w,h))

cv2.imshow("lena_per", lena_per)
cv2.waitKey(0)