# Affine transform
import cv2

lena_img = cv2.imread("../images/lena.bmp")

# 이미지 크기 및 회전 중심 설정
h, w = lena_img.shape[:2]
cX, cY = w / 2, h / 2

# 회전 행렬을 얻어오고, 회전 행렬을 이미지에 적용
rot_mat = cv2.getRotationMatrix2D((cX, cY), 45, 1.0)
rot_mat_0 = cv2.getRotationMatrix2D((0, 0), 45, 1.0)

lena_45 = cv2.warpAffine(lena_img, rot_mat, (w, h))
lena_45_0 = cv2.warpAffine(lena_img, rot_mat_0, (w, h))

cv2.imshow("lena_45", lena_45)
cv2.imshow("lena_45_0", lena_45_0)
cv2.waitKey(0)
cv2.destroyAllWindows()
