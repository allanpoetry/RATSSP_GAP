import pandas as pd

df = pd.read_excel("MapInfo2.xlsx", sheet_name="newd")
data_list = df.values.tolist()

print(data_list)
print(len(data_list))