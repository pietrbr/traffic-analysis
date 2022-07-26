#!/bin/python3
import os, argparse, time, pickle
import pyshark, argparse, os
from tabulate import tabulate
import pandas as pd


class Packet:

    def __init__(self):
        pass


def read_pcapng_and__divide_flows(file_name, file_pathname):
    # lists to store flows
    flow_cmd_a = []
    flow_tel_a = []
    flow_cmd_r = []
    flow_tel_r = []

    # CMD_a
    print("Reading " + file_name + " for flow_cmd_a")
    flow_cmd_a = pyshark.FileCapture(
        file_pathname,
        display_filter=
        "(ip.src_host ==172.16.0.1 && tcp.srcport==44594) || (ip.dst_host ==172.16.0.1 && tcp.dstport==44594)"
    )
    flow_cmd_a.load_packets()

    # TEL_a
    print("Reading " + file_name + " for flow_tel_a")
    flow_tel_a = pyshark.FileCapture(
        file_pathname,
        display_filter=
        "(ip.src_host ==172.16.0.1 && tcp.srcport==44596) || (ip.dst_host ==172.16.0.1 && tcp.dstport==44596)"
    )
    flow_tel_a.load_packets()

    # CMD_r
    print("Reading " + file_name + " for flow_cmd_r")
    flow_cmd_r = pyshark.FileCapture(
        file_pathname,
        display_filter=
        "(ip.src_host ==172.16.0.8 && tcp.srcport==54174) || (ip.dst_host ==172.16.0.8 && tcp.dstport==54174)"
    )
    flow_cmd_r.load_packets()

    # TEL_r
    print("Reading " + file_name + " for flow_tel_r")
    flow_tel_r = pyshark.FileCapture(
        file_pathname,
        display_filter=
        "(ip.src_host ==172.16.0.8 && tcp.srcport==54176) || (ip.dst_host ==172.16.0.8 && tcp.dstport==54176)"
    )
    flow_tel_r.load_packets()

    # show table with numbers of packets for each flow
    print(
        tabulate([["Flow", "# of packets"], ["Collected packets", "N/A"],
                  ["Non-classified packets", "N/A"],
                  ["CMD: BS to UE", len(flow_cmd_a)],
                  ["CMD: UE to BS", len(flow_tel_a)],
                  ["TEL: BS to UE", len(flow_cmd_r)],
                  ["TEL: UE to BS", len(flow_tel_r)]]))
    return len(flow_cmd_a), len(flow_tel_a), len(flow_cmd_r), len(
        flow_tel_r), flow_cmd_a, flow_cmd_r, flow_tel_a, flow_tel_r
    
def create_dataframe(flow: list):
    Timestamp = [float(pckt.sniff_timestamp) for pckt in flow]
    dataframe = pd.DataFrame(zip(Timestamp), columns=["Timestamp"])
    return dataframe


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
    file_pathname = file_dir + "/" + args.file_name

    start = time.time()
    # read .pcapng file and divide flows
    (cnt_cmd_a, cnt_cmd_r, cnt_tel_a, cnt_tel_r, flow_cmd_a, flow_cmd_r,
     flow_tel_a,
     flow_tel_r) = read_pcapng_and__divide_flows(args.file_name, file_pathname)
    print("Time: ", time.time() - start)

    d = {
        'flow_cmd_a': (flow_cmd_a, cnt_cmd_a),
        'flow_tel_a': (flow_tel_a, cnt_tel_a),
        'flow_cmd_r': (flow_cmd_r, cnt_cmd_r),
        'flow_tel_r': (flow_tel_r, cnt_tel_r)
    }


if __name__ == "__main__":
    main()