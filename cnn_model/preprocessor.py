import os

import cv2
import img_preprocess


def cvt_img(input_path, output_path):
    img_names = os.listdir(input_path)

    for img_name in img_names:
        input_name = input_path + "/" + img_name
        output_name = output_path + "/" + img_name
        # print(input_name)

        img = cv2.imread(input_name)
        img, _, _ = img_preprocess.preprocess(img)
        img = img[150:1650, 250:2200, :]
        img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_CUBIC)
        img = cv2.Canny(img, 150, 300)

        cv2.imwrite(output_name, img)


cvt_img("../image/train/true_ng", "../image/train_pre/true_ng")
cvt_img("../image/train/true_ok", "../image/train_pre/true_ok")


# img = cv2.imread("../sample/true_ng/c1_1.jpg")
# img, _, _ = img_preprocess.preprocess(img)
# img = img[150:1650, 250:2200, :]
# img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_CUBIC)

# cv2.imshow("test", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
