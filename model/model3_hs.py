import math
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from img_preprocess import *
from settings import T3_THRESHOLD


def cnt_test(cnt, box, volum_ratio_bound=T3_THRESHOLD):
    """Check the ratio of area of contour and box.

    Args:
        cnt (np.Array): contour
        box (np.Array): square surrounding contour
        volum_ratio_bound (float, optional): threshold value. Defaults to T3_THRESHOLD.

    Returns:
        pred (str): test result
        ratio (float): test score
    """
    area = cv2.contourArea(cnt)
    max_area = cv2.contourArea(box)
    ratio = area / max_area
    if ratio < 1 - volum_ratio_bound:
        pred = "NG"
    else:
        pred = "OK"

    return pred, ratio


def carrier_test(item_img, box, epoxyBox, carrierBox, bright=4, volum_ratio_bound=T3_THRESHOLD, show=False, test=False):
    """test epoxy range within bump and carrier.

    Args:
        item_img (np.Array): preprocessed image of porduct
        box (np.Array): square surrounding censor
        epoxyBox (np.Array): squar surrounding bump
        carrierBox (np.Array): squar surrounding bump but more large area.
        bright (int, optional): maximum of how making image more bright . Defaults to 4.
        volum_ratio_bound (float, optional): threshold value. Defaults to T3_THRESHOLD.
        show (bool, optional): if true show debug image. Defaults to False.
        test (bool, optional): if True work on process_test mode. Defaults to False.

    Returns:
        str: test result 'OK' or 'NG'
        np.Array: debug image
        float: test score
    """
    test_img = colorChange(item_img, "gray")
    cv2.fillPoly(test_img, pts=[epoxyBox], color=(255, 255, 255))
    epoxy_img = test_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[1, 0] : carrierBox[3, 0]].copy()

    cv2.fillPoly(
        test_img, pts=[epoxyBox], color=(int(np.min(epoxy_img)), int(np.min(epoxy_img)), int(np.min(epoxy_img)))
    )
    epoxy_img = test_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[1, 0] : carrierBox[3, 0]].copy()

    for bri in range(bright, 0, -1):
        bri = np.float64(bri)
        epoxy_img_nom = np.clip(epoxy_img * bri, 0, 255).astype(np.uint8)
        epoxy_nom_bin = get_threshold(epoxy_img, epoxy_img_nom, bin_inverse=True)

        contour, hierachy = cv2.findContours(epoxy_nom_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i, cnt in enumerate(contour):
            if cv2.contourArea(cnt) > 10000:
                break

        try:
            len(cnt)
            break
        except:
            continue

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    try:
        pred, ratio = cnt_test(cnt, box, volum_ratio_bound=volum_ratio_bound)

    except:

        if test:
            return pred, test_img, None

        return "NG", test_img, 0

    debug_img = epoxy_img.copy()
    debug_img = colorChange(debug_img, "gray", reverse=True)
    cv2.drawContours(debug_img, [cnt], 0, (0, 0, 255), 3)
    cv2.drawContours(debug_img, [box], 0, (255, 0, 0), 3)
    if show:
        cv2.imshow("carrier_without_epoxy_img", img_resize(debug_img, 800))
        cv2.imshow("carrier_without_epoxy_img_nomalized", img_resize(debug_img, 800))

    if test:
        pass
    return pred, debug_img, ratio


def model_hs(img, show=False, bright=4, test=False, volum_ratio_bound=T3_THRESHOLD):
    """_summary_

    Args:
        img (np.Array): image of porduct
        show (bool, optional): if true show debug image. Defaults to False.
        bright (int, optional): maximum of how making image more bright . Defaults to 4.
        test (bool, optional): if True work on process_test mode. Defaults to False.
        volum_ratio_bound (float, optional): threshold value. Defaults to T3_THRESHOLD.

    Returns:
        str: test result 'OK' or 'NG'
        list of np.Array: debug images
        float: test score
    """
    item_img, carrier_img, cnt, box, epoxyBox, carrierBox, debug_img = find_contours(img, test_3=True, show=show)

    try:
        len(carrier_img)
    except:
        return "NG", [debug_img], 0

    pred, ratio = cnt_test(cnt, box, volum_ratio_bound=volum_ratio_bound)

    if pred == "OK":

        pred, debug_img, ratio = carrier_test(item_img, box, epoxyBox, carrierBox, bright=bright, show=show, test=test)

    if show:
        cv2.putText(item_img, "predicted " + pred, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
        cv2.imshow("result_img", img_resize(item_img, 800))
        key_val = cv2.waitKey(0)
        cv2.destroyAllWindows()

    if test:
        pass
    return pred, [debug_img], ratio


if __name__ == "__main__":
    # test("./team/images/true_ok/GSY827AN7A1492_AAO18758K_PKT15_CM1EQSUA0012_20220711221556_DirectLight_OK.jpg")
    # test("O:/lg/team/images/true_ok/GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg")
    # test("O:/lg/team/images/true_ng/GSY827AN7B0519_AAO12705K_PKT08_CM1EQSUA0011_20220711213213_DirectLight_NG.jpg")

    ok_dir = "./image/module/true_ok/"
    file_names = os.listdir(ok_dir)
    # file_names = [
    #     "GSY827AN7A1492_AAO18758K_PKT15_CM1EQSUA0012_20220711221556_DirectLight_OK.jpg",
    #     "GSY827AN7A2457_AAO08528K_PKT03_CM1EQSUA0011_20220712013351_DirectLight_OK.jpg",
    #     "GSY827AN7A4002_AAO03151K_PKT04_CM1EQSUA0011_20220712220034_DirectLight_OK.jpg",
    #     "GSY827AN7B0050_AAO09322K_PKT07_CM1EQSUA0012_20220711194503_DirectLight_OK.jpg",
    #     "GSY827AN7B0199_AAO04777K_PKT15_CM1EQSUA0011_20220711174834_DirectLight_OK.jpg",
    # ]

    sensor_ratio = []
    bump_ratio = []
    preds = {"OK": 0, "NG": 0}
    for name in file_names:
        img_ok = cv2.imread(ok_dir + name)

        pred, debug_imgs = model_hs(img_ok, show=False, bright=5)
        preds[pred] += 1
        print(preds)

        # try:
        #     pred, debug_imgs = model_hs(img_ok, show=False, bright=5)
        #     preds[pred] += 1
        #     print(preds)
        #     k = 0

        # except:
        #     print(name)
        #     cv2.imshow("error", img_resize(img_ok, 800))

        #     pred, debug_imgs, k = model_hs(img_ok, show=False, bright=5, test=True)

        # if k == ord("q"):
        #     break
    plt.plot(sensor_ratio)
    plt.plot(bump_ratio)
    plt.show()
