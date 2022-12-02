import cv2
import numpy as np


def make_mask(per, n, mode="interior"):
    """이미지에 마진margin을 n만큼 설정해서 출력

    Args:
        per (ndarray): 이미지
        n (int): 마진margin
        mode (str, optional): 기준점. Defaults to 'interior'.

    Returns:
        ndarray: 마진을 설정한 이미지
    """
    if mode == "interior":
        mask = np.zeros(per.shape[:2], np.uint8)
        mask[n : per.shape[0] - n, n : per.shape[1] - n] = 255
        return mask
    elif mode == "margin":
        mask = np.ones(per.shape[:2], np.uint8) * 255
        mask[n : per.shape[0] - n, n : per.shape[1] - n] = 0
        return mask


def white_img_extract(img, debug_img, show=False, margin=10, threshold_color=15):
    """전체 화면에서 흰 화면만 뽑아내기

    Args:
        img (ndarray): BGR 이미지 파일
        show (bool, optional): 그래프 출력 유무. Defaults to False.
        margin (int, optional): 이미지 마진 기준. Defaults to 10.
        threshold_color (int, optional): 히스토그램 자르는 기준. Defaults to 15.

    Returns:
        per: 흰 센서 포함한 이미지
        debug_img: 디버깅 이미지
    """

    # 전처리 과정
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.Canny(blur, 50, 200)

    # 윤곽선 찾아내기
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 이미지 크롭 과정
    box_list, per = [], []
    for cnt in contours:
        pt, hw, ang = cv2.minAreaRect(cnt)
        # minAreaRect 입력값: contours, 반환값: 좌측상단 점, (가로,세로), 각도
        if hw[0] > 1000 and 1000 < hw[1] < 1800:  # 1000
            box = cv2.boxPoints((pt, hw, ang))
            box_list.append(np.int0(box))

    # 이미지 보여주기
    hist_criteria = np.Inf
    for box in box_list:
        img_draw = cv2.drawContours(img, [box], 0, (0, 255, 0), 3)
        debug_img.append(img_draw)
        # 원근변환 이용해서 필요한 이미지 추출
        try:
            box = np.float32(box)
            next_arr = np.array([[0, 0], [1200, 0], [1200, 1600], [0, 1600]], dtype=np.float32)
            per_mat = cv2.getPerspectiveTransform(box, next_arr)
            temp = cv2.warpPerspective(img_draw, per_mat, (1200, 1600))

            mask = make_mask(temp, margin, mode="margin")
            hist = cv2.calcHist([temp], [0], mask, [256], [0, 256])
            # plt.plot(hist)
            hist_val = hist[:-threshold_color].sum()

            if hist_criteria > hist_val:
                hist_criteria = hist_val
                per = cv2.warpPerspective(img_draw, per_mat, (1200, 1600))
        except Exception as e:
            return [], []  # 이미지가 뽑히지 않을 경우 빈 리스트로 반환

    if show:
        cv2.namedWindow("img", flags=cv2.WINDOW_NORMAL)
        cv2.imshow("img", img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    return per, debug_img


def model_ng(img, show=False, huddle=50, margin=10, threshold_color=15):
    """조건2 체크하는 함수: white_img_extract 함수를 통과시킨 센서 이미지의
    색 분포 히스토그램을 calcHist를 이용해서 계산 후 huddle 기준 이하의 이미지만
    OK, 아니면 NG로 반환하는 함수

    Args:
        img (str): 이미지 파일
        show (bool, optional): 그래프 출력 유무. Defaults to True.
        huddle (int, optional): 히스토그램 색 분포 기준. Defaults to 50.
        margin (int, optional): 이미지 마진 기준. Defaults to 10.
        threshold_color (int, optional): 히스토그램 자르는 기준. Defaults to 15.

    Returns:
        str: 조건2 통과하면 OK, 아니면 NG
        debug_img: 디버깅 이미지
    """
    debug_img = []
    per, debug_img = white_img_extract(img, debug_img, show=show)
    if len(per) == 0:
        # if show:
        #     print("이미지가 출력되지 않았습니다.")
        return "NG", debug_img, 100
    else:
        mask = make_mask(per, margin)  # 전체 이미지에서 얼만큼 띄울건지 체크
        mask2 = make_mask(per, margin, mode="margin")
        hist = cv2.calcHist([per], [0], mask, [256], [0, 256])
        hist2 = cv2.calcHist([per], [0], mask2, [256], [0, 256])
        # return hist, hist2  # .sum()
        count = hist[:-threshold_color].sum()
        if count >= huddle:  # huddle을 조절
            if hist2[:100].sum() >= 20000:  # 파라미터 조절
                lang = "OK"
            else:
                lang = "NG"
            # lang = "NG"     # 원래대로 하려면 이거로 바꾸기

        else:
            lang = "OK"
        if show:
            cv2.namedWindow("per", flags=cv2.WINDOW_NORMAL)
            cv2.putText(per, lang, (10, 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)
            cv2.imshow("per", per)
            cv2.waitKey()
            cv2.destroyAllWindows()
        return lang, debug_img, count
