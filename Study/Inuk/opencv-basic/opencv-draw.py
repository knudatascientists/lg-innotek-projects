# 도형 그리기
import cv2
import numpy as np

rgb_img = np.zeros([500, 500, 3], np.uint8)

cv2.rectangle(rgb_img, (10, 10), (100, 100), (0, 0, 255), thickness=1)

cv2.line(rgb_img, (10, 10), (100, 100), (0, 0, 255), thickness=3)

cv2.putText(rgb_img, "hello", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))

cv2.circle(rgb_img, (300, 300), 20, (0, 255, 255))

points1 = np.array([350, 350], [360, 410], [370, 420], [450, 500], np.int32)
cv2.polylines(rgb_img, [points1], True, (255, 0, 0))
