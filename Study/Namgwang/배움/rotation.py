import pandas as pd 
import numpy as np
import cv2
path = r"C:\Users\USER\Documents\GitHub\python_exer\221027\Lenna.png"
img = cv2.imread(path)

(h,w) = img.shape[:2]
(cx,cy) = (w/2, h/2)
# 행렬을 얻는 함수
ret_mat = cv2.getRotationMatrix2D((cx,cy), 45, 1.0)
ret_mat_0 = cv2.getRotationMatrix2D((0,0), 45, 1.0)
# 아핀변환 적용해서 그림 그리기
lena_45 = cv2.warpAffine(img, ret_mat, (w,h))
lena_45_0 = cv2.warpAffine(img, ret_mat_0, (w,h))

cv2.imshow("lena 45", lena_45)
cv2.imshow("lena_45_0", lena_45_0)
cv2.waitKey(0)
