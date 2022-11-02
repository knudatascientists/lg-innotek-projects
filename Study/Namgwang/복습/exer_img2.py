import cv2

# 11.흐림효과 blur
# img = cv2.imread("./Lenna.png", cv2.IMREAD_COLOR)
# dst = cv2.blur(img, (9,9), anchor=(-1,-1), borderType=cv2.BORDER_DEFAULT)

# cv2.imshow("dst", dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 12.가장자리 검출

# img = cv2.imread("./wheal.webp", cv2.IMREAD_COLOR)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# sobel = cv2.Sobel(gray, cv2.CV_8U, 1,0,3)
# laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
# canny = cv2.Canny(img,100,255)

# cv2.imshow("sobel", sobel)
# cv2.imshow("laplacian", laplacian)
# cv2.imshow("canny", canny)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 13.HSV
# img = cv2.imread("./tomato.webp", cv2.IMREAD_COLOR)
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# h,s,v = cv2.split(hsv)
# cv2.imshow("h",h)
# cv2.imshow("s",s)
# cv2.imshow("v",v)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# img = cv2.imread("./tomato.webp", cv2.IMREAD_COLOR)
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# h,s,v = cv2.split(hsv)
# h = cv2.inRange(h,8,20)
# orange = cv2.bitwise_and(hsv,hsv,mask=h)
# orange = cv2.cvtColor(orange, cv2.COLOR_HSV2BGR)

# cv2.imshow("orange", orange)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 배열 병합

img = cv2.imread("./tomato.webp", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

lower_red = cv2.inRange(hsv, (0,100,100), (5,255,255))
upper_red = cv2.inRange(hsv, (170,100,100), (180,255,255))
added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)

red = cv2.bitwise_and(hsv, hsv, mask=added_red)
red = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)

cv2.imshow("red", red)
cv2.waitKey(0)
cv2.destroyAllWindows()
