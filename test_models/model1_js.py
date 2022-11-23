# 모듈 로딩
import os
import random
import sys
import time

import cv2

sys.path.append("../")
import matplotlib.pyplot as plt
import numpy as np

import img_preprocess
import settings


def preprocess_img(img):
    """
    모듈 이미지에서 Carrier와 Sensor만 나오도록 잘라낸 후 전처리
    Args:
        img (3DArray): 검사할 모듈 이미지

    Returns:
        img (3DArray): 모듈 이미지에서 잘라낸 Carrier와 Sensor 이미지
        img_gray (2DArray): 전처리된 모듈 이미지
    """

    # 이미지 잘라내기 (Carrier와 Sensor만 나오도록)
    img = img_preprocess.find_contours(img, show=False)

    # 모듈 없이 촬영된 이미지 불량 처리
    if np.any(img) == None:
        return [], []
    else:
        img
    # 그레이스케일화
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이미지 스무딩
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)

    return img, img_gray


def pre_tem():
    """
    템플릿 매칭에 필요한 템플릿 이미지 전처리
    Returns:
        template (2DArray): 전처리된 템플릿 이미지
    """
    # folder = "../image/template"
    PATH = settings.TEMPLATE_PATH
    FILE_LIST = os.listdir(PATH)
    template = []

    for FILE in FILE_LIST:
        img = cv2.imread(PATH + FILE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template.append(img)
    return template


def match_tem(img, img_gray, template):
    """
    노출된 bump 검출
    Args:
        img (3DArray): 모듈 이미지에서 잘라낸 Carrier와 Sensor 이미지
        img_gray (2DArray): 전처리된 모듈 이미지
        template (2DArray): 전처리된 템플릿 이미지

    Returns:
        cnt (int): 불량으로 매칭된 부분 갯수
        img (3DArray): 모듈 이미지에서 잘라낸 Carrier와 Sensor 이미지
    """
    cnt_h = 0
    cnt_v = 0

    for tem in template:
        w, h = tem.shape[::-1]

        # 템플릿 매칭
        res = cv2.matchTemplate(img_gray, tem, cv2.TM_CCOEFF_NORMED)
        threshold = 0.915  # 0 ~ 1의 값, 높을수록 정확한 결과

        if np.where(res >= threshold):
            loc = np.where(res >= threshold)  # res_h 중 threshold보다 큰 값 위치 저장

            for pt in zip(*loc[::-1]):
                # 결과값에 사각형 그리기
                if w > h:
                    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h + 10), (0, 0, 255), 1)
                    cnt_h += 1
                else:
                    cv2.rectangle(img, pt, (pt[0] + w + 5, pt[1] + h + 10), (0, 0, 255), 1)
                    cnt_v += 1
        cnt = cnt_h + cnt_v
    return cnt, img


def detect_result(cnt, num_OK, num_NG):
    """
    양품, 불량품 판정
    Args:
        cnt (int): 불량으로 매칭된 부분 갯수
        num_OK (int): 양품 갯수
        num_NG (int): 불량품 갯수

    Returns:
        pred (str): 판정 결과 출력
    """
    if cnt >= 1:
        num_NG += 1
        pred = "NG"
    else:
        num_OK += 1
        pred = "OK"
    return pred


def check_img(file, show=False):
    """
    모듈 이미지 검사하여 불량 판정함
    Args:
        file (str): 모듈 이미지 파일

    Returns:
        pred (str): 판정 결과 출력
    """
    num_OK = 0
    num_NG = 0
    template = pre_tem()

    image = cv2.imread(file)
    img, img_gray = preprocess_img(image)

    if img == []:
        num_NG += 1
        pred = "NG"
    else:
        cnt, img = match_tem(img, img_gray, template)
        pred = detect_result(cnt, num_OK, num_NG)
    if show:
        try:
            cv2.imshow("result", img_preprocess.img_resize(image, 800))
        except:
            pass
    return pred


check_img(
    "C:/Users/USER/TeamProject_LG-innotek/product_images/true_ng/GSY827AN7F0152_AAO31742K_PKT10_CM1EQSUA0011_20220717022054_DirectLight_NG.jpg",
    show=True,
)
