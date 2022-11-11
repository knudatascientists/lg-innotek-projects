# resize
import cv2

lena_img = cv2.imread("../images/lena.bmp")

# nearest 보강법 : 가까이에 있는 픽셀로 보강, 화질 보통, 연산 빠름
lena_nearest = cv2.resize(lena_img, dsize=(1000, 1000), interpolation=cv2.INTER_NEAREST)

# cubic 보강법 : 계산해서 보강, 화질 좋음, 연산 느림
lena_cubic = cv2.resize(lena_img, dsize=(1000, 1000), interpolation=cv2.INTER_CUBIC)

cv2.imshow("nearest", lena_nearest)
cv2.imshow("cubic", lena_cubic)
cv2.waitKey(0)
cv2.destroyAllWindows()
