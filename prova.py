import argparse, time
import pandas as pd
from matplotlib import pyplot as plt

# Parsing arguments
parser = argparse.ArgumentParser(description='Boh')

start = time.time()

parser.add_argument('file',
                    metavar='file',
                    type=str,
                    nargs='?',
                    help='file name',
                    default='file.pcapng')
parser.add_argument('-vars',
                    dest='vars',
                    metavar='vars',
                    type=str,
                    nargs='+',
                    action='store',
                    help='vars')
args = parser.parse_args()

print(args.file, args.vars)
if type(args.vars) is not None:
    print(len(args.vars))

print("Time:", time.time() - start)

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