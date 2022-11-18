# 모듈 로딩
import os

import numpy as np
import pandas as pd


def load_data(folder):
    """Load and preprocessing the log data

    Args:
        FOLDER (str): Saved log data location

    Returns:
        dataframe : Loaded and preprocessed the log data
    """
    PATH = os.getcwd() + folder
    FILE_LIST = os.listdir(PATH)
    df = []

    # 로그 데이터 전처리
    for FILE in FILE_LIST:
        data = pd.read_csv(PATH + FILE, header=None)
        data = data.drop_duplicates(subset=0, keep="last")
        data = data.set_index(0)
        df.append(data)

    # 로그 데이터 결합
    df = pd.concat(df, ignore_index="bool", axis=1, join="inner")

    # 인덱스 정렬
    df = df.sort_index(ascending=True)

    # 데이터 타입 변환
    df.iloc[1:, :] = df.iloc[1:, :].astype("float")

    return df


def defect_detect(folder):
    """Defective process output of dataframe

    Args:
        folder (str): Saved log data location
    """
    df = load_data(folder)
    row = df.shape[0]
    col = df.shape[1]

    # 불량공정 입력 컬럼 생성
    df[" "] = np.nan
    df.iloc[2, 290] = "result"
    df.iloc[:2, 290] = " "

    # 불량 공정 출력
    for i in range(row - 3):
        result = []
        for j in range(col - 1):
            a = df.iloc[i + 3, j]
            low = df.iloc[2, j]
            high = df.iloc[1, j]

            if a < low or a > high:
                result.append(df.iloc[0, j])
            else:
                pass
        if result == []:
            df.iloc[i + 3, 290] = "pass"
        else:
            df.iloc[i + 3, 290] = " ".join(result)

    # 결과 저장
    return df.to_csv("output.csv")


defect_detect("\\data_hw01\\Input\\")
