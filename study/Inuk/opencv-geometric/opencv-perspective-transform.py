# perspective transform

import cv2
import numpy as np

lena_img = cv2.imread("../images/lena.bmp")
h, w = lena_img.shape[:2]

src_array = np.array([[0, 0], [0, 511], [511, 0], [511, 511]], np.float32)

dst_array = np.array([[100, 100], [100, 411], [411, 200], [422, 311]], np.float32)

# 원근 행렬을 얻어오고, 행렬을 이미지에 적용
per_mat = cv2.getPerspectiveTransform(src_array, dst_array)
lena_per = cv2.warpPerspective(lena_img, per_mat, (w, h))

cv2.imshow("lena_per", lena_per)
cv2.waitKey(0)
cv2.destroyAllWindows()
