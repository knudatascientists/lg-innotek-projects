### 조건2

### 모듈
import os

import cv2
import img_preprocess
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim


### best 사진과 비교 사진
def preprocessing(img, Similarity=False):
    imageA = cv2.imread(
        "./image/module/true_ok/GSY827AN7A1356_AAO11960K_PKT10_CM1EQSUA0012_20220711210457_DirectLight_OK.jpg"
    )

    img, img1 = img_preprocess.find_contours(imageA, sensor=True, show=False)
    dif, dif1 = img_preprocess.find_contours(img, sensor=True, show=False)
    # dif= cv2.resize(dif, dsize=(1836, 1432))
    dif1 = cv2.resize(dif1, dsize=(1676, 1258))

    tempDiff = cv2.subtract(img1, dif1)

    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(dif1, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    if Similarity:
        try:
            print(f"Similarity: {score:.5f}")
        except:
            pass

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # 차이점 빨간색으로 칠하기
    tempDiff[thresh == 255] = [0, 0, 255]

    #     cv2.imshow("img1", cv2.resize(img1, (960, 540)))
    #     cv2.imshow("dif1", cv2.resize(dif1, (960, 540)))
    #     cv2.imshow("Gray2", cv2.resize(tempDiff, (960, 540)))
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    return tempDiff


### 히스토그램
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


### 검정색 제외한 색깔 추출
def make_mask(per, n=10):
    """이미지에 마진margin을 n만큼 설정해서 출력

    Args:
        per (ndarray): 이미지
        n (int): 마진margin

    Returns:
        ndarray: 마진을 설정한 이미지
    """
    mask = np.zeros(per.shape[:2], np.uint8)
    mask[n : per.shape[0] - n, n : per.shape[1] - n] = 255
    return mask


### 파일 저장
# 양품, 불량 판정 기준
def defect_range(hists):
    hist = np.sum(hists[2][0][6:])
    if hist > 25:
        pred = "NG"
    else:
        pred = "OK"
    return pred


def model_hj(image, show=False):
    """
    모듈 이미지 검사하여 불량 판정함
    Args:
        file (str): 모듈 이미지 파일

    Returns:
        pred (str): 판정 결과 출력
    """

    tempdiff = preprocessing(image)
    mask = make_mask(tempdiff)
    hists = get_hists(tempdiff, mask)
    pred = defect_range(hists)

    debug_img = []

    if show:
        try:
            debug_img.append(tempdiff)
            cv2.imshow("result", img_preprocess.img_resize(image, 800))
        except:
            pass
    return pred, debug_img
