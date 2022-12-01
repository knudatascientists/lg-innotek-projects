import os

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
    """find carrier image of product.

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
        thresh (int, optional): thresh of thresholding. Defaults to -1.
        otsu (bool, optional): if True use otsu thresholding. Defaults to True.

    Returns:
        img_bin (2DArray): image in GRAY
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
    """Check where contour is containing original image's center.

    Args:
        img_shape (2D list): original image's center
        cnt (2D array): contour

    Returns:
        Bool: if True contour is containing original image's center.
    """
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
    """Change image's color type.

    Args:
        img (3D/2D Array): image
        color (str): change type
        reverse (bool, optional): if True change to BGR. Defaults to False.

    Returns:
        img (3D/2D Array): image
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


def getCarrier(item_img, box, test3=False):
    """find product's bump, cropped carrier range.

    Args:
        item_img (3D/2D Array): image
        box (2D Array):rectengle around sensor with min area size
        test3 (bool, optional): if True find more large range for condition 3 test's requierment. Defaults to False.

    Returns:
        sensor_img (3D/2D Array): image
        carrier_img (3D/2D Array): image
        sensorBox (2D Array): range of sensor
        carrierBox (2D Array): range of cropped carrier
        epoxyBox (2D Array): range of bump
    """
    box = np.array(sorted(box, key=lambda x: sum(x)))
    if test3:
        carrier_range = 90
        epoxy_range = carrier_range - 25
    else:
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
    """preprocess for product images

    Args:
        img (3D/2D Array): product image
        show (bool, optional): if true show debug image. Defaults to False.
        test_3 (bool, optional): if true return requierment for condition 3 test. Defaults to False.
        sensor (bool, optional): if true return only sensor image. Defaults to False.

    Returns:
        item_img (3D/2D Array): image
        carrier_img (3D/2D Array): image
        cnt (2D array): contour
        box (2D Array):rectengle around sensor with min area size
        epoxyBox (2D Array): range of bump
        carrierBox (2D Array): range of cropped carrier
        debug_img (3D/2D Array): image
        sensor_img (3D/2D Array): image
        sensorBox (2D Array): range of sensor

    """
    item_img, item_gray, item_bin = preprocess(img)
    contour, hierachy = cv2.findContours(item_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = False
    debug_img = None
    for i, cnt in enumerate(contour):

        if cv2.contourArea(cnt) > 1500000:
            if check_contain(item_img.shape, cnt):
                result = True
                break

    if result:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        sensor_img, carrier_img, sensorBox, carrierBox, epoxyBox = getCarrier(item_img, box, test3=test_3)
        debug_img = item_img.copy()

        cv2.drawContours(debug_img, [carrierBox], 0, (0, 0, 255), 3)
        cv2.drawContours(debug_img, [epoxyBox], 0, (40, 128, 128), 3)
        cv2.drawContours(debug_img, [cnt], 0, (255, 0, 0), 5)
        cv2.drawContours(debug_img, [box], 0, (0, 255, 0), 5)

    else:
        debug_img = item_img.copy()
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
            cv2.imshow("item_img", img_resize(debug_img, 800))
            cv2.imshow("carrier_img", img_resize(carrier_img, 600))
            # key_val = cv2.waitKey(0)
            # cv2.destroyAllWindows()

        except:
            pass
    if test_3:
        return item_img, carrier_img, cnt, box, epoxyBox, carrierBox, debug_img
    if sensor:
        return carrier_img, sensor_img
    return carrier_img


def cnn_preprocess_img(img, image_size: tuple, predict=False):
    """get preprocessed img for cnn model

    Args:
        img (np.array): image array (bgr)
        image_size (tuple): (x, y) image size
        predict (bool, optional): if true return tensorflow dataset shape. Defaults to False.

    Returns:
        _type_: _description_
    """
    _, _, img = preprocess(img)
    img = img[150:1650, 250:2200]
    img = cv2.resize(img, image_size, interpolation=cv2.INTER_CUBIC)

    img = cv2.Canny(img, 50, 200)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    if predict:
        return img.reshape(-1, img.shape[0], img.shape[1], 3)

    return img


def cvt_train_img_path(input_path, output_path, image_size):
    """make train image from directory

    Args:
        input_path (str): raw image path (directory))
        output_path (str): train image path (directory)
        image_size (x, y): x, y tuple
    """
    img_names = os.listdir(input_path)

    for img_name in img_names:
        input_name = input_path + "/" + img_name
        output_name = output_path + "/" + img_name
        # print(input_name)
        img = cv2.imread(input_name)
        img = cnn_preprocess_img(img, image_size)

        cv2.imwrite(output_name, img)
