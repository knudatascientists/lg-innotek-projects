import cv2
import numpy as np


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


def white_img_extract(img, graph=False):
    """전체 화면에서 흰 화면만 뽑아내기

    Args:
        FILENAME (ndarray): BGR 이미지 파일

    Returns:
        ndarray: 흰 센서 포함한 이미지
    """

    # 전처리 과정
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.Canny(blur, 50, 200)

    # 윤곽선 찾아내기
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # image crop
    sl = []
    box_sl = []

    for cnt in contours:
        pt, hw, ang = cv2.minAreaRect(cnt)
        # minAreaRect 입력값: contours, 반환값: 좌측상단 점, (가로,세로), 각도
        if hw[0] > 1000 and hw[1] > 500:
            sl.append([pt, hw, ang])

    for i in sl:
        box = cv2.boxPoints((i[0], i[1], i[2]))
        box_sl.append(np.int0(box))

    # 이미지 보여주기
    for box in box_sl:
        img = cv2.drawContours(img, [box], 0, (0, 255, 0), 3)
    if graph:
        cv2.namedWindow("img", flags=cv2.WINDOW_NORMAL)
        cv2.imshow("img", img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    # 원근변환 이용해서 필요한 이미지 추출
    try:
        box = np.float32(box)
        next_arr = np.array([[0, 0], [1200, 0], [1200, 1600], [0, 1600]], dtype=np.float32)
        per_mat = cv2.getPerspectiveTransform(box, next_arr)
        per = cv2.warpPerspective(img, per_mat, (1200, 1600))
    except Exception as e:
        return []
    # 원근변환한 이미지 보여주기
    if graph:
        cv2.namedWindow("per", flags=cv2.WINDOW_NORMAL)
        cv2.imshow("per", per)
        cv2.waitKey()
        cv2.destroyAllWindows()
    return per


def model_ng(img, graph=False, huddle=100, margin=10):
    """조건2 체크하는 함수: white_img_extract 함수를 통과시킨 센서 이미지의
    색 분포 히스토그램을 calcHist를 이용해서 계산 후 huddle 기준 이하의 이미지만
    OK, 아니면 NG로 반환하는 함수

    Args:
        imgpath (str): 이미지 파일 경로
        graph (bool, optional): 그래프 출력 유무. Defaults to True.
        num (int, optional): 히스토그램 색 분포 기준. Defaults to 160.

    Returns:
        bool: 조건2 통과하면 OK, 아니면 NG
    """
    per = white_img_extract(img, graph=graph)
    if len(per) == 0:
        # return np.inf
        if graph:
            print("이미지가 출력되지 않았습니다.")
        return "NG"
    else:
        mask = make_mask(per, margin)  # 전체 이미지에서 얼만큼 띄울건지 체크
        hist = cv2.calcHist([per], [0], mask, [256], [0, 256])
        # return hist[:-6].sum() hist[6:]
        if hist[:-6].sum() >= huddle:  # huddle을 조절
            if graph:
                cv2.namedWindow("per", flags=cv2.WINDOW_NORMAL)
                cv2.putText(per, "NG", (10, 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)
                cv2.imshow("per", per)
                cv2.waitKey()
                cv2.destroyAllWindows()
            return "NG"
        else:
            if graph:
                cv2.namedWindow("per", flags=cv2.WINDOW_NORMAL)
                cv2.putText(per, "OK", (10, 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)
                cv2.imshow("per", per)
                cv2.waitKey()
                cv2.destroyAllWindows()
            return "OK"
