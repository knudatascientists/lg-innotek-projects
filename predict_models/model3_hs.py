import math
import os
import sys

import cv2
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from img_preprocess import *


def img_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, (0, 0, 0), (0, 0, 100))
    imask = mask > 0
    col = np.zeros_like(img_hsv, np.uint8)
    col[imask] = img_hsv[imask]
    col = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
    return col


def get_angle(pt1, pt2):
    xd = abs(pt2[0] - pt1[0])
    yd = abs(pt2[1] - pt1[1])
    if xd == 0:
        radian = 0.5 * math.pi
    else:
        radian = math.atan(yd / xd)
    return radian


def get_points(cnt):
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)  # 중심점과 각도를 4개의 꼭지점 좌표로 변환
    box = np.int0(box)  # 정수로 변환
    return box


def cnt_test(cnt, box):
    volum_ratio_bound = 0.004
    """_summary_

    Args:
        cnt (_type_): _description_

    Returns:
        _type_: _description_
    """
    area = cv2.contourArea(cnt)
    max_area = cv2.contourArea(box)
    # print(max_area, area,round(area/max_area,3))

    if area / max_area < 1 - volum_ratio_bound + 0.001 or area / max_area > 1 + volum_ratio_bound - 0.001:
        pred = "NG"
    else:
        pred = "OK"
    return pred


def carrier_test(item_img, epoxyBox, carrierBox):
    # print(item_img)
    test_img = item_img.copy()
    test_img[epoxyBox[1, 1] : epoxyBox[3, 1], epoxyBox[0, 0] : epoxyBox[3, 0], :] = 255.0
    carrier_img = test_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[0, 0] : carrierBox[3, 0], :]
    carrier_bin_img = get_threshold(
        carrier_img, colorChange(carrier_img, "gray"), bin_inverse=True, thresh=250, otsu=False
    )
    cv2.imshow("carrier_img", img_resize(carrier_img, 800))
    cv2.imshow("carrier_bin_img", img_resize(carrier_bin_img, 800))
    key_val = cv2.waitKey(0)
    cv2.destroyAllWindows()
    pred = "NG"
    return pred


def model3_hs(img, show=False):
    item_img, carrier_img, cnt, box, epoxyBox, carrierBox = find_contours(img, test_3=True, show=show)

    pred = cnt_test(cnt, box)
    if pred == "OK":
        pred = carrier_test(item_img, epoxyBox, carrierBox)
    cv2.putText(item_img, "predicted " + pred, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
    cv2.imshow("item_img", img_resize(item_img, 800))
    key_val = cv2.waitKey(0)
    cv2.destroyAllWindows()
    return pred
