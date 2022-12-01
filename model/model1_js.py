# 모듈 로딩
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("../")
import img_preprocess
import settings


def preprocess_img(image):
    """
    모듈 이미지에서 Carrier와 Sensor만 나오도록 잘라낸 후 전처리
    Args:
        img (3DArray): 검사할 모듈 이미지

    Returns:
        img (3DArray): 모듈 이미지에서 잘라낸 Carrier와 Sensor 이미지
        img_gray (2DArray): 전처리된 모듈 이미지
    """

    # 이미지 잘라내기 (Carrier와 Sensor만 나오도록)
    img = img_preprocess.find_contours(image, show=False)

    # 모듈 없이 촬영된 이미지 불량 처리
    if np.any(img) == None:
        return [], [], []
    else:
        img
    # 그레이스케일화
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이미지 스무딩
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)

    crop_v1 = img_gray[:, :150]
    crop_v2 = img_gray[:, 1650:]
    crop_h1 = img_gray[:250, :]
    crop_h2 = img_gray[1250:, :]
    crop_h = [crop_h1, crop_h2]
    crop_v = [crop_v1, crop_v2]

    return img, crop_h, crop_v


def pre_tem():
    """
    템플릿 매칭에 필요한 템플릿 이미지 전처리
    Returns:
        template (2DArray): 전처리된 템플릿 이미지
    """
    # folder = "../image/template"
    PATH = settings.TEMPLATE_PATH
    FILE_LIST = os.listdir(PATH)
    tem_h = []
    tem_v = []

    for FILE in FILE_LIST:
        if FILE == ".gitkeep":
            continue

        img = cv2.imread(PATH + FILE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if FILE[0] == "h":
            tem_h.append(img)
        else:
            tem_v.append(img)

    return tem_h, tem_v


def match_tem(img, tem_h, tem_v, crop_h, crop_v):
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

    for img_h in crop_h:
        for tem in tem_h:
            # 템플릿 매칭
            res = cv2.matchTemplate(img_h, tem, cv2.TM_CCOEFF_NORMED)
            threshold = 0.915  # 0 ~ 1의 값, 높을수록 정확한 결과
            w, h = tem.shape[::-1]

            if np.where(res >= threshold):
                loc = np.where(res >= threshold)  # res_h 중 threshold보다 큰 값 위치 저장
                for pt in zip(*loc[::-1]):
                    if w > h:
                        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h + 10), (0, 0, 255), 1)
                        cnt_h += 1

    for img_v in crop_v:
        for tem in tem_v:
            # 템플릿 매칭
            res = cv2.matchTemplate(img_v, tem, cv2.TM_CCOEFF_NORMED)
            threshold = 0.915  # 0 ~ 1의 값, 높을수록 정확한 결과
            w, h = tem.shape[::-1]

            if np.where(res >= threshold):
                loc = np.where(res >= threshold)  # res_h 중 threshold보다 큰 값 위치 저장
                for pt in zip(*loc[::-1]):
                    if w < h:
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


def model_js(image, show=False):
    """
    모듈 이미지 검사하여 불량 판정함
    Args:
        file (str): 모듈 이미지 파일

    Returns:
        pred (str): 판정 결과 출력
    """
    debug_img = []
    num_OK = 0
    num_NG = 0
    tem_h, tem_v = pre_tem()

    img, crop_h, crop_v = preprocess_img(image)

    if img == []:
        num_NG += 1
        pred = "NG"
    else:
        cnt, img = match_tem(img, tem_h, tem_v, crop_h, crop_v)
        pred = detect_result(cnt, num_OK, num_NG)
    debug_img.append(img)
    if show:
        try:
            cv2.imshow("result", img_preprocess.img_resize(img, 800))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            pass
    return pred, debug_img, cnt
