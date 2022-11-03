# https://opencv-python.readthedocs.io/en/latest/doc/01.imageStart/imageStart.html
# --------------------------------------------------------------------------------

# import cv2

# img = cv2.imread('lena1.png', cv2.IMREAD_COLOR) # C:\Users\USER\vscode\study\221028\lena1.png

# cv2.imshow("img", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# --------------------------------------------------------------------------------

## original, gray, unchange 이미지
import cv2

fname = 'lena.jpg'

original = cv2.imread(fname, cv2.IMREAD_COLOR)
gray = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
unchange = cv2.imread(fname, cv2.IMREAD_UNCHANGED)

cv2.imshow('Original', original)
cv2.imshow('Gray', gray)
cv2.imshow('Unchange', unchange)

cv2.waitKey(0)
cv2.destroyAllWindows()
# --------------------------------------------------------------------------------

# ## Matplotlib 사용하기
# from re import U
# import cv2
# from matplotlib import pyplot as plt

# img = cv2.imread('lena.jpg', cv2.IMREAD_COLOR)

# plt.imshow(img)
# plt.xticks([]) # x축 눈금
# plt.yticks([]) # y축 눈금
# plt.show()
# --------------------------------------------------------------------------------

#######
# https://opencv-python.readthedocs.io/en/latest/doc/08.imageProcessing/imageProcessing.html
# ### 이미지 Processing
# import cv2
# import numpy as np

# # Camera 객체를 생성 후 사이즈로 320 x 240 으로 조정.
# cap = cv2.VideoCapture(0)
# cap.set(3, 320)
# cap.set(4, 240)

# while(1):
#     # camera에서 frame capture.
#     ret, frame = cap.read()

#     if ret:

#         # BGR -> HSV로 변환
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         # blue 영역의 from ~ to
#         lower_blue = np.array([110, 50, 50])
#         upper_blue = np.array([130, 255, 255])

#         # 이미지에서 blue영역
#         mask = cv2.inRange(hsv, lower_blue, upper_blue)

#         # bit연산자를 통해서 blue영역만 남김.
#         res = cv2.bitwise_and(frame, frame, mask = mask)

#         cv2.imshow('frame', frame)
#         cv2.imshow('mask', mask)
#         cv2.imshow('res', res)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()
# # --------------------------------------------------------------------------------

# green = np.uint8[[[0, 255, 0]]]
# green_hsv = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
# print(green_hsv)
# # --------------------------------------------------------------------------------

### mountain image
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=rhrkdfus&logNo=221378369642

##### RGB 추출, 합병 함수 #####
# 가로*세로 픽셀 0으로 채운것에 채널로 B, G, R 줘야지 파랑, 초록, 빨강으로 보이게 됨.
# (B, G, R) = cv2.split(image)
# # RGB 합병 함수 -> 원본 나옴.
# merged = cv2.merge([B, G, R])


##### splitting_and_merging.py #####

# import numpy as np
# import cv2

# # 같은 디렉토리 내의 "mountain.jpg"라는 이미지 불러오기
# image = cv2.imread("pisa.jpg")
# (B, G, R) = cv2.split(image)   # OpenCV는 RGB 순서가 아닌 BGR 순서

# # 파랑, 초록, 빨강으로 그림 나누기 -> 회색으로 보임.
# cv2.imshow("Red", R)
# cv2.imshow("Green", G)
# cv2.imshow("Blue", B)
# cv2.waitKey(0)

# # 나눴던 그림 다시 합치기
# merged = cv2.merge([B, G, R])
# cv2.imshow("Merged", merged)
# cv2.waitKey(0)

# # 지금까진 나온 윈도우를 없애고
# cv2.destroyAllWindows()

# # 가로, 세로 픽셀을 0으로 채우고, 채널을 빨강, 초록, 파랑으로
# zeros = np.zeros(image.shape[:2], dtype= "uint8")
# cv2.imshow("Red", cv2.merge([zeros, zeros, R]))
# cv2.imshow("Green", cv2.merge([zeros, G, zeros]))
# cv2.imshow("Blue", cv2.merge([B, zeros, zeros]))

# cv2.waitKey(0)
# --------------------------------------------------------------------------------

##### 다양한 효과 넣기 #####
# colorspaces.py

# import numpy as np
# import cv2

# # 같은 디렉토리 내의 "pisa.jpg"라는 이미지 불러오기
# image = cv2.imread("pisa.jpg")
# cv2.imshow("Original", image)

# # 회색조로 바꾸기
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Gray", gray)

# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# cv2.imshow("HSW", hsv)

# lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
# cv2.imshow("L*a*b", lab)
# cv2.waitKey(0)