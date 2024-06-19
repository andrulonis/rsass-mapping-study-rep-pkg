import pandas as pd

df_og_data = pd.read_csv("data/2023_data/all_filtered_by_title.csv")
df_new_data_og_keywords = pd.read_csv("data/2024_data_og_keywords/all_filtered_by_title.csv")
df_new_data_with_keywords = pd.read_csv("data/all_filtered_by_title.csv")

diff12 = pd.concat([df_og_data,df_new_data_og_keywords], axis=0)
diff12 = diff12.drop_duplicates(keep=False,subset=['title'],ignore_index=True)

diff23 = pd.concat([df_new_data_og_keywords,df_new_data_with_keywords], axis=0)
diff23 = diff23.drop_duplicates(keep=False,subset=['title'],ignore_index=True)

diff13 = pd.concat([df_og_data,df_new_data_with_keywords], axis=0)
diff13 = diff13.drop_duplicates(keep=False,subset=['title'],ignore_index=True)

diff12.to_csv("data/diff_og_data_to_new_data_og_keywords.csv",index=False)
diff23.to_csv("data/diff_new_data_og_keywords_to_new_data_with_keywords.csv",index=False)
diff13.to_csv("data/diff_og_data_to_new_data_with_keywords.csv",index=False)
