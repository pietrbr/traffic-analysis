import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

df = pd.read_csv("./new_csv/csv/1010123456007_metrics.csv")
print(df.columns)
# df["Timestamp"] = df["Timestamp"] - min(df["Timestamp"])
# plt.plot(df["Timestamp"], df["ul_sinr"])
plt.plot(df["ul_sinr"])
# plt.plot(df["power_multiplier"])
plt.show()