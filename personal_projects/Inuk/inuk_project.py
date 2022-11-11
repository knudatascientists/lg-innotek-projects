import pandas as pd
import numpy as np
import os


def read_log_files(input_path):
    """read log data files from dir

    Args:
        input_path (str): log files path

    Returns:
        pd.DataFrame: all log files droped duplicates and na
    """
    files = os.listdir(input_path)  # 파일 목록 불러오기
    df_list = []

    # 파일 목록으로 파일 불러와서 리스트에 저장
    for file in files:
        df = pd.read_csv(input_path + file, header=None)
        df.drop_duplicates(subset=0, keep="last", inplace=True)  # 중복 제거하고 마지막 측정 결과만 사용
        df.set_index(0, inplace=True)
        df_list.append(df)

    # 리스트에 있는 파일 하나로 합치기
    data = pd.concat(df_list, axis=1)
    # 검사 누락된 항목 제거
    data.dropna(inplace=True)

    return data


def log_result(data):
    """add result columns to dataframe

    Args:
        data (pd.DataFrame): all logs data

    Returns:
        pd.DataFrame_: add result data
    """
    data_c = data.copy()

    row_len = data_c.shape[0]

    low = data_c.iloc[0, :].astype(float)  # 최소값
    high = data_c.iloc[1, :].astype(float)  # 최대값
    barcode = data_c.iloc[2, :]  # 모듈이름

    result = [np.NAN, np.NAN, "result"]  # 출력할 결과값

    for i in range(3, row_len):
        row = data_c.iloc[i, :].astype(float)
        c1 = row > low
        c2 = row < high
        row_boolean = ~(c1 & c2)

        # 조건에 부합하는 모듈만 뽑아냄
        row_result = list(barcode[row_boolean])

        if len(row_result) == 0:
            result.append(np.NAN)  # 값이 없을경우 none값
        else:
            result.append(" ".join(row_result))  # 값이 있으면 문자열 합쳐서

    data_c["result"] = result

    return data_c


def save_output(data, output_path):
    data.to_csv(output_path + "output.csv")


INPUT_PATH = "./Input/"
OUTPUT_PATH = "./output/"

data = read_log_files(INPUT_PATH)
data_result = log_result(data)
save_output(data_result, OUTPUT_PATH)
