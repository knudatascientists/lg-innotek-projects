import pandas as pd 
import numpy as np
import cv2

img = cv2.imread("./moon.webp")
# 1.imshow 실행
# cv2.imshow("moon", img)
# cv2.waitKey(0)           # 키 누를때까지 대기
# cv2.destroyAllWindows()  # 키를 누르면 창 닫기

# 2.imshow 실행2 (flag 다루기)
# img2 = cv2.imread("./moon.webp", flags=cv2.IMREAD_GRAYSCALE)
# img3 = cv2.imread("./moon.webp", flags=cv2.IMREAD_REDUCED_COLOR_8)
# cv2.imshow("moon2", img2)
# cv2.waitKey(0)           
# cv2.destroyAllWindows() 
# cv2.imshow("moon3", img3)
# cv2.waitKey(0)           
# cv2.destroyAllWindows() 

# imwrite 실행
# cv2.imwrite("./moon.jpeg", img, [cv2.IMWRITE_JPEG_QUALITY, 95])

# 3.flip 실행
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# dst = cv2.flip(img,-5)
# cv2.imshow("flip",dst)
# cv2.waitKey(0)           
# cv2.destroyAllWindows() 

# 4.rotate 실행
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# height, width, channel = img.shape
# matrix = cv2.getRotationMatrix2D((width/2, height/2),90,1)
# dst = cv2.warpAffine(img, matrix, (width, height))

# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 5.확대 & 축소 실행
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# height, width, channel = img.shape

# dst = cv2.pyrUp(img, dstsize=(width*2, height*2), borderType=cv2.BORDER_DEFAULT)
# dst2 = cv2.pyrDown(img)

# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.imshow("dst2", dst2)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 6.크기 조절
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# dst = cv2.resize(img, dsize=(640,480), interpolation=cv2.INTER_AREA)
# dst2 = cv2.resize(img, dsize=(0,0), fx=0.3, fy=0.7, interpolation=cv2.INTER_LINEAR)

# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.imshow("dst2", dst2)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 7.자르기
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# dst = img.copy()
# roi = img[100:400, 300:600]
# dst[0:300, 0:300] = roi

# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 8.색상공간 변환
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# dst = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 9. 역상
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)
# dst = cv2.bitwise_not(img)
# cv2.imshow("img", img)
# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()

# 10. 이진화 threshold
# img = cv2.imread("./water.webp", cv2.IMREAD_COLOR)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, dst = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()


img = cv2.imread("./Lenna.png", cv2.IMREAD_COLOR)

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
ret, dst = cv2.threshold(rgb,100,255,cv2.THRESH_BINARY)

cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()