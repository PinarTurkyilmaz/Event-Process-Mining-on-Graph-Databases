import pandas as pd
a = pd.read_csv("log_graph_v4.csv")
b = pd.read_csv("impact_without_blank.csv")
#b = b.dropna(axis=1)
merged = a.merge(b, on=['CI_ID','SC', 'CI_type', 'CI_name', 'en_ID'], how='left')
merged.to_csv("output_v2.csv", index=False)
        
         
