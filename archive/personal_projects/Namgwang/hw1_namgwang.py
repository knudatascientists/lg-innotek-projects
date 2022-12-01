# 과제1 - 개인 프로젝트: 로그 파일을 취합해서 결과 생성
# 요구사항1 : 6개의 파일들을 1개의 통합 결과(.csv)으로 만들어라
# 요구사항2 : 중복된 바코드에서 선별하여 시간상으로 마지막으로 측정된 데이터를 사용해야 함
# 요구사항3 : Log들은 바코드 순(사전 순)으로 정렬
# 요구사항4 : 어떤 바코드들은 l공정에는 없지만, m공정에는 있는 경우가 있다. 이런 경우는 통합결과에서 제거
# 요구사항5 : result 열을 추가하여 각 공정의 측정값이 모두 정상일 경우 pass를 기입
# 요구사항6 : 불량일 경우 어떤 항목이 불량이었는지 result 열에 남겨야 하며, 다중 항목 불량인 경우 모든 항목을 다 남겨야 함
import os

import pandas as pd

# 파일 경로
PATH = "./log_merge_proj_data/Input/"

# 1. csv 파일 합치는 과정 - 요구사항1 만족
p = pd.DataFrame()
for idx, v in enumerate(os.listdir(PATH)):
    df = pd.read_csv(PATH + v, header=None)
    # drop_duplicates를 사용하여 요구사항2 만족
    df.drop_duplicates(subset=[0], keep="last", inplace=True)
    df.set_index(0, inplace=True)
    # sort_index를 이용하여 요구사항3 만족
    df.sort_index(inplace=True)
    # concat에서 join="inner"조건을 사용해서 요구사항4 만족
    if idx != 0:
        p = pd.concat([p, df], axis=1, join="inner")
    else:
        p = pd.concat([p, df], axis=1)


# 요구사항5, 요구사항6을 만족하기 위해 apply에 적용할 함수 작성
def ftt(row):
    row = row.astype(float)
    barcode = p.iloc[
        0,
    ]
    hi = p.iloc[
        1,
    ].astype(float)
    lo = p.iloc[
        2,
    ].astype(float)
    s = ""
    d = 0
    for idx, val in enumerate(row):
        if lo.iloc[idx] < val < hi.iloc[idx]:
            continue
        else:
            s += barcode.iloc[idx] + " "
            d = 1
    if d == 1:
        return s.rstrip()
    else:
        return "pass"


# 합친 파일에 apply를 적용해서 result 생성하기
barcode = p.iloc[
    0,
]
hi = p.iloc[
    1,
].astype(float)
lo = p.iloc[
    2,
].astype(float)
g = p.iloc[
    3:,
].copy()
h = g.apply(ftt, axis=1)

# 만든 result 컬럼을 csv파일에 추가
h = pd.concat([p, h], axis=1)
h.iloc[0:3, len(h.columns) - 1] = [0, 0, "result"]

# 파일 저장
h.to_csv("log_result.csv", header=False)
