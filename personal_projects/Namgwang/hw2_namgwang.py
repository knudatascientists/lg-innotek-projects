import cv2
import numpy as np

#%%


def image_linear(FILENAME, w_a, h_a, graph=False):
    """bilinear interpolation을 수행하는 함수

    Args:
        FILENAME (str): 이미지 파일 경로
        w_a (int): 가로 width
        h_a (int): 세로 height
        graph (bool, optional): 그래프 출력 유무. Defaults to False.

    Returns:
        ndarray: resized image
    """
    img = cv2.imread(FILENAME)
    h, w = img.shape[:2]

    mat_x = np.linspace(0, w, w_a)
    mat_y = np.linspace(0, h, h_a)
    x_hat = np.clip(np.int0(np.floor(mat_x)), 0, w - 1)
    y_hat = np.clip(np.int0(np.floor(mat_y)), 0, h - 1)

    x_hat_l = np.full_like([0] * len(x_hat), w - 1)
    x_hat_l[0:-1] = x_hat[1:]
    y_hat_l = np.full_like([0] * len(y_hat), h - 1)
    y_hat_l[0:-1] = y_hat[1:]

    a, b = mat_x - x_hat, mat_y - y_hat
    a, b = a.reshape(1, a.shape[0], 1), b.reshape(b.shape[0], 1, 1)

    mat_a = img[y_hat, :][:, x_hat]
    mat_b = img[y_hat_l, :][:, x_hat]
    mat_c = img[y_hat, :][:, x_hat_l]
    mat_d = img[y_hat_l, :][:, x_hat_l]
    # 공식
    dct = (1 - a) * ((1 - b) * mat_a) + b * ((1 - a) * mat_b) + a * ((1 - b) * mat_c) + a * b * mat_d
    dct = np.uint8(dct)
    if graph:
        # cv2.namedWindow("resize", flags=cv2.WINDOW_NORMAL)
        cv2.imshow("resize", dct)
        cv2.waitKey()
        cv2.destroyAllWindows()
    return dct


#%%

if "__main__" == __name__:
    image_linear("flower.webp", 1200, 1800, graph=True)
