import math

import cv2
import numpy as np


def img_mask(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, (0, 0, 0), (0, 0, 100))
    imask = mask > 0
    col = np.zeros_like(img_hsv, np.uint8)
    col[imask] = img_hsv[imask]
    col = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
    return col


def check_contain(img_shape, cnt):
    center_bound = 100
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    # center = (int(x), int(y))
    radius = int(radius)
    center_diff = ((int(img_shape[0] / 2) - int(y)) ** 2 + (int(img_shape[1] / 2) - int(x)) ** 2) ** 0.5
    # print(center, (img_shape[1]/2,img_shape[0]/2), center_diff)
    if center_diff < center_bound:
        return True
    return False


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


def cnt_test(cnt):
    volum_ratio_bound = 0.005
    """_summary_

    Args:
        cnt (_type_): _description_

    Returns:
        _type_: _description_
    """
    area = cv2.contourArea(cnt)
    arcLen = cv2.arcLength(cnt, closed=True)
    box = get_points(cnt)
    s_box = sorted(box, key=lambda x: x[0] + x[1])
    point1, point2 = s_box[0], s_box[2]

    angle = get_angle(point1, point2)
    sin, cos = math.sin(angle), math.cos(angle)

    cal_max_box = ((arcLen**2) / 4 - 2 * area) * (sin * cos) + area
    max_box = cv2.contourArea(box)

    if cal_max_box / max_box < 1 - volum_ratio_bound or cal_max_box / max_box > 1 + volum_ratio_bound:
        pred = "NG"
    else:
        pred = "ok"
    return point1, point2, pred


def find_contours(item_img, item_bin):
    # img = cv2.resize(img, (0,0), fx = 0.3, fy = 0.3, interpolation=cv2.INTER_CUBIC)

    col = img_mask(item_img)
    # contour, hierachy = cv2.findContours(item_bin, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contour, hierachy = cv2.findContours(item_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    for i, cnt in enumerate(contour):

        if cv2.contourArea(cnt) > 1500000:
            if check_contain(item_img.shape, cnt):
                cv2.drawContours(item_img, [cnt], 0, (255, 0, 0), 5)
                result = True
                break

    pred = "NG"
    if result:
        point1, point2, pred = cnt_test(cnt)

    return pred


def model3_hs(item_img, item_bin):
    result = find_contours(item_img, item_bin)
    return result
