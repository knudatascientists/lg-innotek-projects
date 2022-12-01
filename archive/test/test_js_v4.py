# 모듈 로딩
import os
import random
import time

import cv2
import img_preprocess
import matplotlib.pyplot as plt
import model3_hs
import numpy as np


def make_dir(file_path):
    """
    결과 저장할 폴더 생성
    Args:
        file_path (str): 결과 저장할 폴더 위치
    """
    if os.path.isdir(file_path + "result_type1"):
        os.mkdir(file_path + "result_type1/ok")
        os.mkdir(file_path + "result_type1/ng")
    else:
        os.makedirs(file_path + "result_type1/ok")
        os.makedirs(file_path + "result_type1/ng")


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
    folder = "\\tem_image\\"
    PATH = os.getcwd() + folder
    FILE_LIST = os.listdir(PATH)
    template = []

    for FILE in FILE_LIST:
        img = cv2.imread(PATH + FILE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template.append(img)
    return template


# 노출된 bump 검출
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
        threshold = 0.905  # 0 ~ 1의 값, 높을수록 정확한 결과

        if np.where(res >= threshold):
            loc = np.where(res >= threshold)  # res_h 중 threshold보다 큰 값 위치 저장

            for pt in zip(*loc[::-1]):
                # 결과값에 사각형 그리기
                if w > h:
                    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h + 10), (0, 0, 255), 1)
                    cnt_h += 1
                else:
                    cv2.rectangle(
                        img, pt, (pt[0] + w + 5, pt[1] + h + 10), (0, 0, 255), 1
                    )
                    cnt_v += 1
        cnt = cnt_h + cnt_v
    return cnt, img


# 양품, 불량 판정 기준
def defect_range(cnt, file_path, name, image, num_OK, num_NG):
    """
    불량 검출 유무에 따라 양품, 불량 판정
    Args:
        cnt (int): 불량으로 매칭된 부분 갯수
        file_path (str): 저장할 폴더 위치
        name (str): 품번
        image (3DArray): 기존 이미지
        num_OK (int): 양품 갯수
        num_NG (int): 불량품 갯수

    Returns:
        num_OK (int): 양품 갯수 출력
        num_NG (int): 불량품 갯수 출력
    """
    if cnt >= 1:
        cv2.imwrite(file_path + "result_type1/ng/" + name, image)
        num_NG += 1
    else:
        cv2.imwrite(file_path + "result_type1/ok/" + name, image)
        num_OK += 1
    return num_OK, num_NG


def detect_result(cnt, num_OK, num_NG):
    """
    양품, 불량품 판정
    Args:
        cnt (int): 불량으로 매칭된 부분 갯수
        num_OK (int): 양품 갯수
        num_NG (int): 불량품 갯수

    Returns:
        str: 판정 결과 출력
    """
    if cnt >= 1:
        num_NG += 1
        pred = "NG"
    else:
        num_OK += 1
        pred = "OK"
    return pred


def test(path):
    img = cv2.imread(path)
    pred = model3_hs(img, show=False, thresh=4.0)
    print(pred)


# 이미지 로딩 후 검사
def check_img(kind="overkill"):
    """
    제품 이미지 파일 로딩하여 검사
    Args:
        kind (str, optional): _description_. Defaults to "overkill".

    Returns:
        _type_: _description_
    """
    # random.seed(time.time_ns() % 10000)
    num_OK = 0
    num_NG = 0
    template = pre_tem()
    if kind == "all":
        paths = os.listdir("./product_images/")
        img_paths = []
        for p in paths:
            file_path = "./product_images/" + p + "/"
            img_paths = list(map(lambda x: [file_path + x, p], os.listdir(file_path)))
            make_dir(file_path)

        count = 0
        while count > len(ip):
            ip = random.choice(img_paths)
            image = cv2.imread(ip[0])
            img, img_gray = preprocess_img(image)

            if img == []:
                cv2.imwrite(file_path + "result_type1/ng/" + img_paths[i], image)
                num_NG += 1
            else:
                cnt, img = match_tem(img, img_gray, template)
                num_OK, num_NG = defect_range(
                    cnt, file_path, ip[0], image, num_OK, num_NG
                )
                count += 1
                break

    else:
        file_path = "./product_images/" + kind + "/"
        img_paths = os.listdir(file_path)
        make_dir(file_path)

        for i in range(len(img_paths) - 1):
            image = cv2.imread(file_path + img_paths[i])
            img, img_gray = preprocess_img(image)

            if img == []:
                cv2.imwrite(file_path + "result_type1/ng/" + img_paths[i], image)
                num_NG += 1
                pred = "NG"
            else:
                cnt, img = match_tem(img, img_gray, template)
                num_OK, num_NG = defect_range(
                    cnt, file_path, img_paths[i], image, num_OK, num_NG
                )

            return pred
