import pandas as pd

df=pd.read_csv("output_v3.csv")
#gk=df["en_ID"].value_counts()
#gk.to_csv("count_en.csv", index=True)
b=pd.read_csv("count_en.csv")
merged = df.merge(b, on=['en_ID'], how='left')
merged.to_csv("output_v3.csv", index=False)
