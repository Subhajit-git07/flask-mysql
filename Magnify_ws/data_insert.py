import pandas as pd
import numpy as np

data = pd.read_csv("/data/knowledge/masterdata.csv")
noise_data = pd.read_csv("/data/knowledge/SSPNoise.csv")

noise_data_L1 = noise_data.iloc[:,0:2][noise_data['Level']==1]
noise_data_L2 = noise_data.iloc[:,0:2][noise_data['Level']==2]
noise_data_L3 = noise_data.iloc[:,0:2][noise_data['Level']==3]

data_L1_raw = data.loc[data.AllSTHash.isin(noise_data_L1['Hash'])]
data_L1_raw = data_L1_raw[["AllSTHash","_raw"]]
data_L1_raw = data_L1_raw.drop_duplicates(subset=['AllSTHash'], keep='first')

data_L2_raw = data.loc[data.AribaSTHash.isin(noise_data_L2['Hash'])]
data_L2_raw = data_L2_raw[["AribaSTHash","_raw"]]
data_L2_raw = data_L2_raw.drop_duplicates(subset=['AribaSTHash'], keep='first')

data_L3_raw = data.loc[data.ThirdHash.isin(noise_data_L3['Hash'])]
data_L3_raw = data_L3_raw[["ThirdHash","_raw"]]
data_L3_raw = data_L3_raw.drop_duplicates(subset=['ThirdHash'], keep='first')


import pymysql
connection = pymysql.connect(host='127.0.0.1',user='jenkins1234',password='12345',db='abcdef_logs')
cur=connection.cursor()

for i in data_L3_raw["_raw"]:
    query = "INSERT INTO noise_db (log_str) VALUES (%s);"
    param = (i,)
    cur.execute(query,param)
connection.commit()
connection.close()
print("Inserted successfully")
