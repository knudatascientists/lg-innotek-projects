### 조건2

### 모듈
import os

import cv2
import matplotlib.pyplot as plt

# import model3_hs
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

import img_preprocess

### 불러올 경로
# PATH = "./product_images/true_ng/result/ok/"
# for i in os.listdir(PATH):
#     print(PATH + i)
#     preprocessing(PATH+i)

### best 사진과 비교 사진
def preprocessing(imgg):
    imageA = cv2.imread(
        "./product_images/true_ok/GSY827AN7A1356_AAO11960K_PKT10_CM1EQSUA0012_20220711210457_DirectLight_OK.jpg"
    )

    img, img1 = img_preprocess.find_contours(imageA, sensor=True)
    dif, dif1 = img_preprocess.find_contours(imgg, sensor=True)
    # dif= cv2.resize(dif, dsize=(1836, 1432))
    dif1 = cv2.resize(dif1, dsize=(1676, 1258))

    tempDiff = cv2.subtract(img1, dif1)

    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(dif1, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    print(f"Similarity: {score:.5f}")

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # 차이점 빨간색으로 칠하기
    tempDiff[thresh == 255] = [0, 0, 255]

    cv2.imshow("img1", cv2.resize(img1, (960, 540)))
    cv2.imshow("dif1", cv2.resize(dif1, (960, 540)))
    cv2.imshow("Gray2", cv2.resize(tempDiff, (960, 540)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return tempDiff


### 비교 예시
preprocessing("./product_images/true_ok/GSY827AN7A1385_AAO16043K_PKT02_CM1EQSUA0012_20220711205902_DirectLight_OK.jpg")

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
def make_mask(per, n):
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


tempdiff = preprocessing(
    "./product_images/true_ok/GSY827AN7A1385_AAO16043K_PKT02_CM1EQSUA0012_20220711205902_DirectLight_OK.jpg"
)
mask = make_mask(tempdiff, 10)
hists = get_hists(tempdiff, mask=mask)
for hist, c in hists:
    plt.plot(hist[6:], color=c)
    plt.title("gray")
    plt.show()

### 빨간색 개수 구하기
hist = np.sum(hists[2][0][6:])
hist
# 정상
# 7번 - 33/ 8번 -  31/ 9번 - 29/ 10번 - 35/ 11번 - 39/ 12번 - 41/ 13번 - 32/ 14번 - 38/ 15번 - 31/ 16번 -27/
# 불량
# 7번 - 34 / 8번 - 26 / 9번 - 398/ 10번 - 40/ 11번 - 40/ 12번 - 125/ 13번 - 54/ 14번 - 38/ 15번 - 26/ 16번 -35/

### NG or OK 판정
def check_num(hist):
    if hist > 25:
        return "NG"
    else:
        return "OK"


check_num(hist)

### 파일 저장
# 양품, 불량 판정 기준
def defect_range(hist, file_path, name, imageB, num_OK, num_NG):
    """
    불량 검출 유무에 따라 양품, 불량 판정
    Args:
        cnt (int): _description_
        file_path (str): _description_
        name (str): _description_
        image (_type_): _description_
        num_OK (int): _description_
        num_NG (int): _description_

    Returns:
        int: _description_
    """
    if hist > 25:
        cv2.imwrite(file_path + "result/ng/" + name, imageB)
        num_NG += 1
    else:
        cv2.imwrite(file_path + "result/ok/" + name, imageB)
        num_OK += 1
    return num_OK, num_NG
