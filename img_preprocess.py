import cv2
import matplotlib.pyplot as plt
import numpy as np


def img_resize(img, resize_size=1600):
    """return image in specific size maintaining image shape ratio

    Args:
        img (3DArray): image in BGR
        resize_size (int, optional): target size {max (height, weight)}

    Returns:
        img (3DArray): image in BGR
    """
    width_origin = img.shape[1]
    height_origin = img.shape[0]
    hw_list = [height_origin, width_origin]

    img_ratio = float(resize_size) / max(hw_list)
    max_index = hw_list.index(max(hw_list))
    if max_index == 0:
        img = cv2.resize(img, (int(width_origin * img_ratio), resize_size), interpolation=cv2.INTER_CUBIC)
    else:
        img = cv2.resize(img, (resize_size, int(height_origin * img_ratio)), interpolation=cv2.INTER_CUBIC)

    return img


def find_large_label(img, img_bin, show_img=False):
    """_summary_

    Args:
        img (3DArray): image in BGR
        img_bin (3DArray): thresholded image
        show_img (bool, optional): if True show image with label. Defaults to False.

    Returns:
        _type_: _description_
    """
    test_img = img.copy()
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(
        img_bin,
    )
    stats = sorted(stats, key=lambda x: x[4], reverse=True)
    if show_img:
        for i, rec in enumerate(stats[:2]):
            x, y, w, h, area = rec
            cv2.rectangle(test_img, (x, y, w, h), (0, 0, 255), thickness=8)

        cv2.imshow("items", img_resize(test_img, 600))
        cv2.imshow("items_bin", img_resize(img_bin, 600))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # print(stats[0])
    if stats[0][1] == 0:
        return stats[1]
    return stats[0]


def get_threshold(img, gray, bin_inverse=True, thresh=-1, otsu=True):
    """return image with threshold
    Args:
        img (3DArray): image in BGR
        gray (2DArray): image in GRAY
        bin_inverse (bool, optional): if True white will be black. Defaults to True.

    Returns:
        _type_: _description_
    """

    if otsu:
        if bin_inverse:
            _, img_bin = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        else:
            _, img_bin = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    else:
        if bin_inverse:
            _, img_bin = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)
        else:
            _, img_bin = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

    return img_bin


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


def colorChange(img, color, reverse=False):
    """_summary_

    Args:
        img (3D/2D Array): image
        color (str): change type
        reverse (bool, optional): if True change to BGR. Defaults to False.

    Returns:
        _type_: _description_
    """
    if reverse:
        if color == "hsv":
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        elif color == "ycrcb":
            img = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
        elif color == "gray":
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    else:
        if color == "hsv":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        elif color == "ycrcb":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        elif color == "gray":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


def get_hists(img, mask=None, ranges=[0, 255]):
    """show image's distribution

    Args:
        img (3D/2D Array): image
        mask (cv2.inrange, optional): image where you wanna get hist. Defaults to None.
        ranges (list, optional): _description_. Defaults to [0, 255].

    Returns:
        hists (list): list of each component's hist
    """
    colors = ["b", "g", "r"]
    img_planes = cv2.split(img)
    hists = []
    for (p, c) in zip(img_planes, colors):
        try:
            hist = cv2.calcHist(
                [p],
                [0],
                mask,
                [256],
                ranges,
            )
            hists.append([hist, c])

        except:
            pass

    return hists


def preprocess(img):
    """return item image

    Args:
        img (3DArray): image in BGR

    Returns:
        _type_: _description_
    """
    gray = colorChange(img, color="gray")
    img_bin = get_threshold(img, gray, bin_inverse=True)
    large_stat = find_large_label(img, img_bin)

    try:
        item_img = img[
            large_stat[1] : large_stat[1] + large_stat[3], large_stat[0] : large_stat[0] + large_stat[2], :
        ].copy()
        item_gray = gray[
            large_stat[1] : large_stat[1] + large_stat[3], large_stat[0] : large_stat[0] + large_stat[2]
        ].copy()
    except:
        item_img, item_gray = img, gray

    item_bin = get_threshold(item_img, item_gray, bin_inverse=False)
    return item_img, item_gray, item_bin


def getCarrier(item_img, box):
    box = np.array(sorted(box, key=lambda x: sum(x)))
    carrier_range = 80
    epoxy_range = carrier_range - 20
    sensorBox = box.copy()
    carrierBox = box.copy()
    epoxyBox = box.copy()
    sensorBox[0] = np.array([box[1, 0], box[1, 1]])
    sensorBox[1] = np.array([box[0, 0], box[0, 1]])
    sensorBox[2] = np.array([box[2, 0], box[2, 1]])
    sensorBox[3] = np.array([box[3, 0], box[3, 1]])
    carrierBox[0] = np.array([box[1, 0] - carrier_range, box[1, 1] + carrier_range + 7])
    carrierBox[1] = np.array([box[0, 0] - carrier_range, box[0, 1] - carrier_range - 7])
    carrierBox[2] = np.array([box[2, 0] + carrier_range, box[2, 1] - carrier_range - 7])
    carrierBox[3] = np.array([box[3, 0] + carrier_range, box[3, 1] + carrier_range + 7])
    epoxyBox[0] = np.array([box[1, 0] - epoxy_range, box[1, 1] + epoxy_range + 7])
    epoxyBox[1] = np.array([box[0, 0] - epoxy_range, box[0, 1] - epoxy_range - 7])
    epoxyBox[2] = np.array([box[2, 0] + epoxy_range, box[2, 1] - epoxy_range - 7])
    epoxyBox[3] = np.array([box[3, 0] + epoxy_range, box[3, 1] + epoxy_range + 7])

    sensor_img = item_img[sensorBox[1, 1] : sensorBox[3, 1], sensorBox[0, 0] : sensorBox[3, 0], :].copy()
    carrier_img = item_img[carrierBox[1, 1] : carrierBox[3, 1], carrierBox[0, 0] : carrierBox[3, 0], :].copy()
    return sensor_img, carrier_img, sensorBox, carrierBox, epoxyBox


def find_contours(img, show=True, test_3=False, sensor=False):
    item_img, item_gray, item_bin = preprocess(img)
    contour, hierachy = cv2.findContours(item_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    for i, cnt in enumerate(contour):

        if cv2.contourArea(cnt) > 1500000:
            if check_contain(item_img.shape, cnt):
                result = True
                break

    if result:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        sensor_img, carrier_img, sensorBox, carrierBox, epoxyBox = getCarrier(item_img, box)
        if show:
            test_img = item_img.copy()
            cv2.drawContours(test_img, [carrierBox], 0, (0, 0, 255), 3)
            cv2.drawContours(test_img, [epoxyBox], 0, (40, 128, 128), 3)
        if show:
            cv2.drawContours(test_img, [cnt], 0, (255, 0, 0), 5)
            cv2.drawContours(test_img, [box], 0, (0, 255, 0), 5)

    else:
        cnt, box, item_img, sensor_img, carrier_img, sensorBox, carrierBox, epoxyBox = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    if show:
        try:
            # cv2.putText(item_img, "predicted " + pred, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
            cv2.imshow("item_img", img_resize(test_img, 800))
            cv2.imshow("carrier_img", img_resize(carrier_img, 600))
            key_val = cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            pass
    if test_3:
        return item_img, carrier_img, cnt, box, epoxyBox, carrierBox
    if sensor:
        return carrier_img, sensor_img
    return carrier_img
