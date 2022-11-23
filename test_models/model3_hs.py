import math
import os
import sys

import cv2
import matplotlib.pyplot as plt
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
    volum_ratio_bound = 0.01
    """_summary_

    Args:
        cnt (_type_): _description_

    Returns:
        _type_: _description_
    """
    area = cv2.contourArea(cnt)
    max_area = cv2.contourArea(box)
    # print(max_area, area,round(area/max_area,3))

    if area / max_area < 1 - volum_ratio_bound or area / max_area > 1 + volum_ratio_bound:
        pred = "NG"
    else:
        pred = "OK"
    return pred


def show_color_gif(img):
    img_gray = colorChange(img, "gray")
    j = 10
    for i in range(0, 255 // j):
        mask = cv2.inRange(img_gray, (i * j), (i * j + j))
        test_img = np.ones_like(img_gray, np.uint8) * 255
        test_img[mask > 0] = img_gray[mask > 0]

        test_img = colorChange(test_img, "gray", reverse=True)

        cv2.imshow("test_img", img_resize(test_img, resize_size=600))

        k = cv2.waitKey(j * 20)
        if k == ord("q"):
            break
    cv2.destroyAllWindows()
    return k


def get_carrier_templet():
    pass


def carrier_test(item_img, box, epoxyBox, carrierBox, thresh=4.0, show=False):
    test_img = colorChange(item_img, "gray")

    # print(get_hists(test_img)[0])
    # test_img[epoxyBox[1, 1] : epoxyBox[3, 1], epoxyBox[1, 0] : epoxyBox[3, 0]] = 255.0
    cv2.fillPoly(test_img, pts=[epoxyBox], color=(255, 255, 255))
    epoxy_img = test_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[1, 0] : carrierBox[3, 0]].copy()

    # test_img[epoxyBox[1, 1] : epoxyBox[3, 1], epoxyBox[1, 0] : epoxyBox[3, 0]] = np.uint8(np.min(epoxy_img))
    cv2.fillPoly(
        test_img, pts=[epoxyBox], color=(int(np.min(epoxy_img)), int(np.min(epoxy_img)), int(np.min(epoxy_img)))
    )
    epoxy_img = test_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[1, 0] : carrierBox[3, 0]].copy()

    epoxy_img_nom = np.clip(epoxy_img * thresh, 0, 255).astype(np.uint8)
    epoxy_nom_bin = get_threshold(epoxy_img, epoxy_img_nom, bin_inverse=True)

    contour, hierachy = cv2.findContours(epoxy_nom_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contour):
        if cv2.contourArea(cnt) > 100000:
            # print(cv2.contourArea(cnt))
            break

    try:
        len(cnt)
    except:
        return "NG"

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    try:
        pred = cnt_test(cnt, box)
    except:
        pred = "NG"
        quit()
    # print(epoxy_gray.max())
    if show:
        epoxy_img = colorChange(epoxy_img, "gray", reverse=True)
        cv2.drawContours(epoxy_img, [cnt], 0, (0, 0, 255), 3)
        cv2.drawContours(epoxy_img, [box], 0, (255, 0, 0), 3)
        cv2.imshow("carrier_without_epoxy_img", img_resize(epoxy_img, 800))
        cv2.imshow("carrier_without_epoxy_img_nomalized", img_resize(epoxy_img_nom, 800))
    return pred


def model_hs(img, show=False, thresh=4.0):
    item_img, carrier_img, cnt, box, epoxyBox, carrierBox = find_contours(img, test_3=True, show=show)

    try:
        len(carrier_img)
    except:
        return "NG"

    pred = cnt_test(cnt, box)
    if pred == "OK":
        pred = carrier_test(item_img, box, epoxyBox, carrierBox, thresh=thresh, show=show)
    if show:
        cv2.putText(item_img, "predicted " + pred, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        cv2.imshow("result_img", img_resize(item_img, 800))
        key_val = cv2.waitKey(0)
        cv2.destroyAllWindows()
    return pred


def test(path):
    img = cv2.imread(path)
    pred = model_hs(img, show=True, thresh=4.0)
    print(pred)


if __name__ == "__main__":
    # test("./team/images/true_ok/GSY827AN7A1492_AAO18758K_PKT15_CM1EQSUA0012_20220711221556_DirectLight_OK.jpg")
    test("O:/lg/team/images/true_ok/GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg")
    test("O:/lg/team/images/true_ng/GSY827AN7B0519_AAO12705K_PKT08_CM1EQSUA0011_20220711213213_DirectLight_NG.jpg")

    # ok_dir = "./team/images/true_ok/"
    # # file_names = os.listdir(ok_dir)
    # file_names = [
    #     "GSY827AN7A1492_AAO18758K_PKT15_CM1EQSUA0012_20220711221556_DirectLight_OK.jpg",
    #     "GSY827AN7A2457_AAO08528K_PKT03_CM1EQSUA0011_20220712013351_DirectLight_OK.jpg",
    #     "GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg",
    #     "GSY827AN7B0050_AAO09322K_PKT07_CM1EQSUA0012_20220711194503_DirectLight_OK.jpg",
    #     "GSY827AN7B0199_AAO04777K_PKT15_CM1EQSUA0011_20220711174834_DirectLight_OK.jpg",
    # ]

    # for name in file_names[:10]:
    #     img_ok = cv2.imread(ok_dir + name)
    #     pred = model3_hs(img_ok, show=True, thresh=4.0)
    #     print(pred)
