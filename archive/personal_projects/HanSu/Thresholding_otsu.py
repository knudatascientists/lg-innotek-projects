# Thresholding with otsu
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def otsu(img):
    # 라이브러리 사용
    """기존 라이브러리 사용 threshold

    Args:
        img (3Darray): 이미지(GBR)
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    T, lenna_otsu = cv2.threshold(img, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    hist = cv2.calcHist([img], [0], None, [255], [0, 256])

    # histogram
    plt.plot(hist)
    plt.vlines(T, 0, 3000, colors="red")  # 임계값
    plt.text(T, 2600, str(T))
    plt.show()
    cv2.imshow("lenna_otsu", lenna_otsu)
    cv2.waitKey()
    cv2.destroyAllWindows()


def my_otsu(img):
    """라이브러리 미사용 threshold - otsu

    Args:
        img (3Darray): 이미지(GBR)
    """

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # hisogram 그리기
    f_img = img.flatten()
    counts = pd.value_counts(sorted(f_img)).sort_index()
    hist = np.array(
        [[counts.loc[i]] if i in counts.index else [0] for i in range(1, 256)],
        np.float32,
    )
    plt.plot(hist)

    # 분산을 통한 임계값 계산
    result = pd.DataFrame(columns=["임계값", "내부 분산", "외부 분산"])
    hist = hist.flatten()
    c = sum(hist)
    for i in range(0, 255):
        background = hist[:i]
        foreground = hist[i:]

        weight_b = sum(background) / c
        weight_f = sum(foreground) / c
        if sum(background) == 0:
            mu_b = 0
            var_b = 0
        else:
            var_b = sum([(j - mu_b) ** 2 * hist[j] for j in range(i)]) / sum(background)
            mu_b = sum([j * hist[j] for j in range(i)]) / sum(background)

        if sum(foreground) == 0:
            mu_f = 0
            var_f = 0
        else:
            mu_f = sum([j * hist[j] for j in range(i, 255)]) / sum(foreground)
            var_f = sum([(j - mu_f) ** 2 * hist[j] for j in range(i, 255)]) / sum(
                foreground
            )

        result.loc[len(result)] = [
            i,
            weight_b * var_b + weight_f * var_f,
            weight_b * weight_f * ((mu_b - mu_f) ** 2),
        ]

    thresh = result["내부 분산"].argmin()
    plt.vlines(thresh, 0, 3000, colors="red")
    plt.text(thresh, 2600, str(thresh))
    plt.show()

    threshold_img = img.copy()
    o_shape = threshold_img.shape
    threshold_img = np.where(threshold_img.flatten() >= thresh, 255, 0)

    threshold_img = threshold_img.reshape(o_shape).astype(np.uint8)
    cv2.imshow("lenna_my_otsu", threshold_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print(result)


if __name__ == "__main__":
    img = cv2.imread("./study/test_img/Lenna.png")
    img = cv2.imread("./study/test_img/face_detect01.jpg")
    otsu(img)
    my_otsu(img)
