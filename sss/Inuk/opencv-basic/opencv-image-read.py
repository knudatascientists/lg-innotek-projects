# image 읽기, 출력
import cv2

# 이미지 파일 읽기
lena_img = cv2.imread("../images/lena.bmp")

# 이미지 파일 출력
cv2.imshow("lena", lena_img)

cv2.waitKey(0)  # 키 입력 대기
cv2.destroyAllWindows()  # 모든 창 종료

# 이미지 파일을 jpeg 형식으로 쓰기
# (이미지명, Data, [형식, 퀄리티])
cv2.imwrite("./images/lena_jpg.jpg", lena_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite("./images/lena_png.png", lena_img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
