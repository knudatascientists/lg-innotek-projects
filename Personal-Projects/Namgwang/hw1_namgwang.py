# 과제1
import pandas as pd 
import numpy as np
import os

# 파일 경로
PATH = "./log_merge_proj_data/Input/"

# csv 파일 합치기
p = pd.DataFrame()
for idx, v in enumerate(os.listdir(PATH)):
    df = pd.read_csv(PATH + v, header=None)
    df.drop_duplicates(subset=[0], keep="last", inplace=True)
    df.set_index(0, inplace=True)
    df.sort_index(inplace=True)
    if idx != 0:
        p = pd.concat([p,df], axis=1, join="inner")
    else:
        p = pd.concat([p,df], axis=1)



# apply에 적용할 함수 작성
def ftt(row):
    row = row.astype(float)
    barcode = p.iloc[0,]
    hi = p.iloc[1,].astype(float)
    lo = p.iloc[2,].astype(float)
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
barcode = p.iloc[0,]
hi = p.iloc[1,].astype(float)
lo = p.iloc[2,].astype(float)
g = p.iloc[3:,].copy()
h = g.apply(ftt, axis=1 )
h = pd.concat([p,h], axis=1)
h.iloc[0:3,len(h.columns)-1] = [0,0,"result"]

# 파일 저장
h.to_csv("log_result.csv", header=False)