import time
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# dataframes
flow_1 = [1, 2, 3, 4]
flow_2 = [1, 2, 3, 4]
flow_3 = [1, 2, 5, 4]
flow_4 = [1, 2, 3, 4]

df = pd.DataFrame(list(zip(flow_1, flow_2, flow_3, flow_4)),
                  columns=["flow_1", "flow_2", "flow_3", "flow_4"])
print(df)

fig = plt.figure()

# dictonary
daje = {"a": 1, "b": 2}

for help in daje:
    print(daje[help])

string = 'daje!'
last = string[-1]
prima = string[0:-1]

print(string, last, prima)