import os
import pandas as pd
import numpy as np
input_path = './log_merge_proj_data/Input/'
input_datas = os.listdir(input_path)

def get_data(data_name):
    data = pd.read_csv(input_path + data_name, header =2)
    data_limit = pd.read_csv(input_path + data_name, header =None, names= data.columns).iloc[:2,1:]
    data.drop_duplicates(['barcode'], keep = 'last', inplace= True)
    data.reset_index(inplace = True, drop = True)
    return data, data_limit

data, data_limit = get_data(input_datas[0])
barcode = set(data['barcode'])
for data_name in input_datas[1:]:
    data, data_limit = get_data(data_name)
    barcode = barcode & set(data['barcode'])

datas = []
data_limits = []
for data_name in input_datas:
    data,data_limit = get_data(data_name)
    data.set_index('barcode',inplace = True)
    data_limits.append(data_limit)    
    data = data.loc[barcode,:]
    data.sort_index(inplace = True)
    datas.append(data)

total = pd.concat(datas, axis = 1)
total_limit = pd.concat(data_limits, axis = 1)

result = ['pass' for i in range(len(barcode))]
for col in  total_limit.columns:
    low, high = list(map(float, total_limit[col]))
    result = [' '.join([r,col]) if d <= low or d >= high else r for r, d in zip(result, total[col])]
result = [r if r == 'pass' else r[5:] for r in result]

total['result'] = result
total.reset_index(inplace=True)
total_limit=total_limit.rename(index = {0:'low limit', 1:'high limit'}).reset_index()

total_limit['result']=['','']
total_limit.rename(columns = {'index': 'barcode'}, inplace = True)

output = pd.concat([total_limit,total])
output.to_csv('output.csv', index = False, header=False)