import time
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# dataframes
flow_1 = [1, 2, 3, 4]
flow_2 = [1, 2, 3, 4]
flow_3 = [1, 2, 5, 4]
flow_4 = [1, 2, 3, 4]

# df = pd.DataFrame(list(zip(flow_1, flow_2, flow_3, flow_4)),
#                   columns=["flow_1", "flow_2", "flow_3", "flow_4"])
# print(df)
# df["new_column"] = df.loc[:, "flow_1"] * 5
# print(df)
# df = df[["flow_1", "new_column", "flow_2", "flow_3", "flow_4"]]
# print(df)
# for col in df:
#     print("\n\n Daje")
#     print(col, type(col))
#     print(df[col])

sns.set_theme(style="whitegrid")
diamonds = sns.load_dataset("diamonds")
f, ax = plt.subplots(figsize=(6.5, 6.5))
sns.despine(f, left=True, bottom=True)
clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]
sns.scatterplot(x="carat",
                y="price",
                hue="clarity",
                size="depth",
                palette="ch:r=-.2,d=.3_r",
                hue_order=clarity_ranking,
                sizes=(1, 8),
                linewidth=0,
                data=diamonds,
                ax=ax)
print("Finito")

# fig = plt.figure()

# # DICT
# daje = {"a": 1, "b": 2}

# for help in daje:
#     print(daje[help])

# string = 'daje!'
# last = string[-1]
# prima = string[0:-1]

# print(string, last, prima)

# # PICKLE
# df.to_pickle("daje")
# df_read = pd.read_pickle("daje")
# print("\ndf\n", df, "\ndf_read\n", df_read)