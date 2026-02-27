import pandas as pd
import os

folder_path = "/Users/pranaya/Downloads/sales_data"

all_files = os.listdir(folder_path)

df_list = []

for file in all_files:
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder_path,file))
        df['Month'] = file.replace(".csv","")
        df_list.append(df)
combined_df = pd.concat(df_list,ignore_index=True)
combined_df.to_csv("combined_sale.csv",index=False)
print("All files combined successfully")
