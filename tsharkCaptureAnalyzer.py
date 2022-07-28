from pcapngRead import *
from pcapngVisualize import *
import os, argparse, time
import pyshark
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():

    # Parsing arguments
    parser = argparse.ArgumentParser(
        description=
        'Read pcapng files, filter and divide packets into flows, and plot graphs.'
    )
    parser.add_argument(
        'file_name',
        metavar='file_name',
        type=str,
        nargs='?',
        help='file path and name',
        default='session-1/tshark_bs/tshark_log_2022_07_20_19_34_17.pcapng')
    parser.add_argument('-tcp',
                        dest='tcp_vars',
                        metavar='tcp_vars',
                        type=str,
                        nargs='+',
                        action='store',
                        help='Any of the followings: analysis_ack_rrt')
    args = parser.parse_args()
    print(args.file_name, args.tcp_vars)

    # create paths and names variables
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_pathname = f"{file_dir}/{args.file_name}"

    # read .pcapng file and divide flows
    (cnt_cmd_a, cnt_cmd_r, cnt_tel_a, cnt_tel_r, flow_cmd_a, flow_cmd_r,
     flow_tel_a,
     flow_tel_r) = read_pcapng_and_divide_flows(args.file_name, file_pathname)

    # dictonary with flow names and flows
    flows = {
        'flow_cmd_a': (flow_cmd_a, cnt_cmd_a),
        'flow_tel_a': (flow_tel_a, cnt_tel_a),
        'flow_cmd_r': (flow_cmd_r, cnt_cmd_r),
        'flow_tel_r': (flow_tel_r, cnt_tel_r)
    }
    dfs = {}

    for flow in flows:
        print(flows[flow])
        dfs[flow] = create_dataframe(flows[flow][0])
        print(dfs)

    # plot graphs
    if args.tcp_vars is not None:
        for var in args.tcp_vars:
            for flow_name in flows:
                flow, cnt = flows[flow_name]
                values, timestamps, avg, stdev = tcp_table_stats(
                    var, flow, cnt, flow_name)
                tcp_plot_stats(values, timestamps, flow_name, avg, stdev)


if __name__ == "__main__":
    main()