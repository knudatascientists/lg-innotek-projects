# 14. 배열 병합 연습

import cv2
import numpy as np
import pandas as pd
# red
# img = cv2.imread("./rainbow.png", cv2.IMREAD_COLOR)
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower_red = cv2.inRange(hsv, (0,0,0), (5,255,255))
# upper_red = cv2.inRange(hsv, (170,0,0), (180,255,255))
# added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)

# red = cv2.bitwise_and(hsv, hsv, mask=added_red)
# red = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)

# cv2.imshow("red", red)
# cv2.waitKey()
# cv2.destroyAllWindows()

# orange 및 여러 색깔
# orange_lower, orange_upper = (5,0,0), (20,255,255)
# yellow_lower, yellow_upper = (20,0,0), (30,255,255)
# green_lower, green_upper = (30,0,0), (70,255,255)
# forest_lower, forest_upper = (70,0,0), (85,255,255)
# blue_lower, blue_upper = (85,0,0), (100,255,255)
# navy_lower, navy_upper = (100,0,0), (120,255,255)
# violet_lower, violet_upper = (120,0,0), (145,255,255)
# def color_img(lower, upper):
#     img = cv2.imread("./rainbow.png", cv2.IMREAD_COLOR)
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     color = cv2.inRange(hsv, lower, upper)
#     dst = cv2.bitwise_and(hsv, hsv, mask=color)
#     dst = cv2.cvtColor(dst, cv2.COLOR_HSV2BGR)
#     cv2.imshow("red", dst)
#     cv2.waitKey()
#     cv2.destroyAllWindows()

# color_img(violet_lower, violet_upper)

# 15. 채널 분리 & 병합

# img = cv2.imread("tomato.webp", cv2.IMREAD_COLOR)
# b,g,r = cv2.split(img)
# inverse = cv2.merge((r,g,b))

# cv2.imshow("b", b)
# cv2.imshow("g", g)
# cv2.imshow("r", r)
# cv2.imshow()
# cv2.imshow("inverse", inverse)
# cv2.waitKey()
# cv2.destroyAllWindows()


# img = cv2.imread("tomato.webp", cv2.IMREAD_COLOR)
# dst = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# y, cr, cb = cv2.split(dst)
# dst = cv2.merge((cb,cr,y))
# inverse = cv2.cvtColor(dst, cv2.COLOR_YCrCb2BGR)

# cv2.imshow("y", y)
# cv2.imshow("cr", cr)
# cv2.imshow("cb", cb)
# cv2.imshow("inverse", inverse)
# cv2.waitKey()
# cv2.destroyAllWindows()


# img = cv2.imread("tomato.webp", cv2.IMREAD_COLOR)
# dst = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# y, cr, cb = cv2.split(dst)
# dst = cv2.merge((cb,cr,y))
# inverse = cv2.cvtColor(dst, cv2.COLOR_YCrCb2BGR)

# cv2.imshow("y", y)
# cv2.imshow("cr", cr)
# cv2.imshow("cb", cb)
# cv2.imshow("inverse", inverse)
# cv2.waitKey()
# cv2.destroyAllWindows()


# img = cv2.imread("tomato.webp", cv2.IMREAD_COLOR)
# b = img[:,:,0]
# g = img[:,:,1]
# r = img[:,:,2]
# height, width, channel = img.shape
# zero = np.zeros((height, width,1), dtype=np.uint8)
# dst = cv2.merge((b,g,zero))

# cv2.imshow("b", b)
# cv2.imshow("g", g)
# cv2.imshow("r", r)
# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()


# 16. numpy를 이용한 이미지 생성
# empty_mat = np.empty((500,500), np.float32)
# zeros_mat = np.zeros((500,500))
# ones_mat = np.ones((500,500))
# ones_mat_int = np.ones((500,500), np.uint8)
# full_mat = np.full((500,500,3), (166,83,246), dtype=np.uint8)
# fuzzy_wuzzy = np.full((500,500,3), (31,65,135), dtype=np.uint8)
# pink_flamingo = np.full((500,500,3), (253,116,252), dtype=np.uint8)
# turquoise = np.full((500,500,3), (231,218,108), dtype=np.uint8)
# cv2.imshow("empty_mat", empty_mat)
# cv2.imshow("zeros_mat", zeros_mat)
# cv2.imshow("ones_mat", ones_mat)
# cv2.imshow("ones_mat_int", ones_mat_int)
# cv2.imshow("full_mat", full_mat)
# cv2.imshow("fuzzy_wuzzy", fuzzy_wuzzy)
# cv2.imshow("pink_flamingo", pink_flamingo)
# cv2.imshow("turquoise", turquoise)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 17. 도형그리기
# img = np.zeros((720,1024,3), dtype=np.uint8)
# img = cv2.line(img, (100,100), (900,100), (0,0,255), 3, cv2.LINE_AA)
# img = cv2.circle(img, (300,300), 50, (0,255,0), cv2.FILLED, cv2.LINE_4)
# img = cv2.rectangle(img, (500,200), (1000,400), (255,0,0), 5, cv2.LINE_8)
# img = cv2.ellipse(img, (800,300), (100,50), 0,90,180,(255,255,0),2)

# pts1 = np.array([[100,500], [300,500], [200,600]])
# pts2 = np.array([[600,500], [800,500], [700,600]])

# img = cv2.polylines(img, [pts1], True, (100,136,255), 2)
# img = cv2.fillPoly(img, [pts2], (234,215,118), cv2.LINE_AA, shift=1)

# cv2.imshow('img', img)
# cv2.imwrite('drawing.jpg', img)
# cv2.waitKey()
# cv2.destroyAllWindows()


# img = np.zeros((720,1024,3), dtype=np.uint8)
# cv2.putText(img, "mouse", (500,400), cv2.FONT_ITALIC, 1, (255,255,255), 3)
# cv2.imshow('img', img)
# cv2.waitKey()
# cv2.destroyAllWindows()


# 18. 기하학적 변환 (아핀 변환, 원근 변환)
img = cv2.imread("wheal.webp", cv2.IMREAD_COLOR)
h, w, c = img.shape

print(h,w)  # 1280, 1920
src_array = np.array([[0,0],[w,0],[w,h],[0,h]], np.float32)
dst_array = np.array([[300,200],[400,200],[500,500],[200,500]], np.float32)

per_mat = cv2.getPerspectiveTransform(src_array, dst_array)

per_mat = cv2.getPerspectiveTransform(dst_array, src_array)
per = cv2.warpPerspective(img, per_mat, (w,h))

cv2.imshow("per", per)
cv2.waitKey()
cv2.destroyAllWindows()