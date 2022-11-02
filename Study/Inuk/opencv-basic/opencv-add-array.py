# 이미지 연산 - add array
import cv2
import numpy as np

# opencv는 rgb가 아니라 bgr순서
# 0번 채널 b 생성
b_img = np.zeros([300, 300, 3], np.uint8)
b_img[:, :, 0].fill(255)

# 1번 채널 g 생성
g_img = np.zeros([300, 300, 3], np.uint8)
g_img[:, :, 1].fill(255)

# b와 g를 더한 이미지 생성
bg_img = b_img + g_img

cv2.imshow("blue", b_img)
cv2.imshow("greed", g_img)
cv2.imshow("blue+green", bg_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
