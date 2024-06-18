import pandas as pd

df1 = pd.read_csv("data/all_filtered_by_title.csv")
df2 = pd.read_csv("data/2023_data/all_filtered_by_title.csv")

diff = pd.concat([df1,df2], axis=0)

diff = diff.drop_duplicates(keep=False,subset=['title'],ignore_index=True)

diff.to_csv("data/diff_csvs.csv",index=False)
