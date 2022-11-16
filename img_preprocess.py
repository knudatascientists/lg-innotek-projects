import cv2


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


def get_threshold(img, gray, bin_inverse=True):
    """return image with threshold
    Args:
        img (3DArray): image in BGR
        gray (2DArray): image in GRAY
        bin_inverse (bool, optional): if True white will be black. Defaults to True.

    Returns:
        _type_: _description_
    """
    if bin_inverse:
        _, img_bin = cv2.threshold(gray, -1, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    else:
        _, img_bin = cv2.threshold(gray, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return img_bin


def preprocess(img):
    """return item image

    Args:
        img (3DArray): image in BGR

    Returns:
        _type_: _description_
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
