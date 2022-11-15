import cv2


def find_large_label(img, gray, img_bin, bin_inverse=True):

    _, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bin)
    stats = sorted(stats, key=lambda x: x[4], reverse=True)
    if bin_inverse == True:
        return stats[1]
    else:
        return stats[0]


def get_threshold(img, gray, bin_inverse=True):
    if bin_inverse:
        _, img_bin = cv2.threshold(
            gray, -1, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
    else:
        _, img_bin = cv2.threshold(gray, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return img_bin


def preproces(img, bin_inverse=True, only_bin=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = get_threshold(img, gray, bin_inverse=True)

    large_stat = find_large_label(img, gray, img_bin)
    try:
        item_img = img[
            large_stat[1] : large_stat[1] + large_stat[3],
            large_stat[0] : large_stat[0] + large_stat[2],
            :,
        ].copy()
        item_gray = gray[
            large_stat[1] : large_stat[1] + large_stat[3],
            large_stat[0] : large_stat[0] + large_stat[2],
        ].copy()
    except:
        item_img, item_gray = img, gray

    item_bin = get_threshold(item_img, item_gray, bin_inverse=False)
    return item_img
