import argparse
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

# Parsing arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file_name',
                    metavar='file_name',
                    type=str,
                    nargs='?',
                    help='file path and name',
                    default='first-session/csv_bs/1010123456007_metrics.csv')
# parser.add_argument('--sum',
#                     dest='accumulate',
#                     action='store_const',
#                     const=sum,
#                     default=max,
#                     help='sum the integers (default: find the max)')
args = parser.parse_args()

df = pd.read_csv(args.file_name)
print(df.columns)
df["Timestamp"] = df["Timestamp"] - min(df["Timestamp"])
plt.plot(df["Timestamp"], df["ul_sinr"])
plt.show()
plt.plot(df["ul_sinr"])
plt.show()
# plt.plot(df["power_multiplier"])