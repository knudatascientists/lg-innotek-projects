# 이미지 연산 - image roi(region of interest)
import cv2

lena_img = cv2.imread("../images/lena.bmp")
lena_img2 = cv2.copyTo(lena_img, None)

# 이미지의 특정 영역을 얻을 때에는 : 사용
# numpy_array[y_start:y_end, x_start:x_end, channal_start, channal_end]
lena_img2[10:100, :, :] = 0

cv2.imshow("lena", lena_img)
cv2.imshow("lena2", lena_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
