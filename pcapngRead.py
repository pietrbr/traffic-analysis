#!/bin/python3
import os, argparse, time, pickle
import pyshark, argparse, os
from tabulate import tabulate
import pandas as pd

PORTS_DICT = {
    "session-0/log_2022_07_14_first_bs.pcap":
    None,
    "session-0/log_2022_07_14_first_ue.pcap":
    None,
    "session-1/tshark_bs/tshark_log_2022_07_20_19_34_17.pcapng":
    [44584, 44588, 54166, 54168],
    "session-1/tshark_bs/tshark_log_2022_07_20_19_59_22.pcapng":
    [44590, 54170, 44592, 54172],
    "session-1/tshark_bs/tshark_log_2022_07_20_20_21_20.pcapng":
    [44594, 54174, 44596, 54176],
    "session-1/tshark_ue/tshark_log_2022_07_20_19_31_27.pcapng":
    [44584, 44588, 54166, 54168],
    "session-1/tshark_ue/tshark_log_2022_07_20_19_59_25.pcapng":
    [44590, 54170, 44592, 54172],
    "session-1/tshark_ue/tshark_log_2022_07_20_20_21_17.pcapng":
    [44594, 54174, 44596, 54176],
    "session-2/tshark-bs/tshark_log_2022_07_26_20_01_29.pcapng":
    None,
    "session-2/tshark-bs/tshark_log_2022_07_26_20_22_51.pcapng":
    None
}
FILES_DICT = {
    "session-0/log_2022_07_14_first_bs.pcap":
    "session-0/log_2022_07_14_first_bs.pcap",
    "session-0/log_2022_07_14_first_ue.pcap":
    "session-0/log_2022_07_14_first_ue.pcap",
    "session-1/tshark_bs/5m":
    "session-1/tshark_bs/tshark_log_2022_07_20_19_34_17.pcapng",
    "session-1/tshark_bs/10m":
    "session-1/tshark_bs/tshark_log_2022_07_20_19_59_22.pcapng",
    "session-1/tshark_bs/7.5m":
    "session-1/tshark_bs/tshark_log_2022_07_20_20_21_20.pcapng",
    "session-1/tshark_ue/5m":
    "session-1/tshark_ue/tshark_log_2022_07_20_19_31_27.pcapng",
    "session-1/tshark_ue/10m":
    "session-1/tshark_ue/tshark_log_2022_07_20_19_59_25.pcapng",
    "session-1/tshark_ue/7.5m":
    "session-1/tshark_ue/tshark_log_2022_07_20_20_21_17.pcapng",
    "session-2/tshark_bs/5m":
    "session-2/tshark-bs/tshark_log_2022_07_26_20_01_29.pcapng",
    "session-2/tshark_bs/10m":
    "session-2/tshark-bs/tshark_log_2022_07_26_20_22_51.pcapng"
}


class Packet:

    def __init__(self):
        pass


def read_pcapng_and__divide_flows(file_name, file_pathname, pickle_flag=False):
    # parser.add_argument('-tcp',
    #                     dest='tcp_vars',
    #                     metavar='tcp_vars',
    #                     type=str,
    #                     nargs='+',
    #                     action='store',
    #                     help='Any of the followings: analysis_ack_rrt')

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


def create_dataframe(flow):
    Timestamp = [float(pckt.sniff_timestamp) for pckt in flow]
    dataframe = pd.DataFrame(zip(Timestamp), columns=["Timestamp"])
    return dataframe


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description=
        'Read pcapng files, filter and divide packets into flows, and plot graphs.'
    )
    parser.add_argument('file_path',
                        metavar='file_path',
                        type=str,
                        nargs='?',
                        help='files path',
                        default='session-0')
    args = parser.parse_args()
    print(args.file_name, args.tcp_vars)
    session_dir = os.getcwd() + "/" + args.file_path + "/"

    # create variables for paths and names
    # file_dir = os.path.dirname(os.path.realpath(__file__))
    # file_pathname = file_dir + "/" + args.file_path

    # read .pcapng file and divide flows
    for file in os.listdir(session_dir):
        if file.endswith('.pcapng'):
            (cnt_cmd_a, cnt_cmd_r, cnt_tel_a, cnt_tel_r, flow_cmd_a,
             flow_cmd_r, flow_tel_a,
             flow_tel_r) = read_pcapng_and__divide_flows(args.file_name,
                                                         session_dir,
                                                         pickle_flag=True)
            flows = {
                'flow_cmd_a': (flow_cmd_a, cnt_cmd_a),
                'flow_tel_a': (flow_tel_a, cnt_tel_a),
                'flow_cmd_r': (flow_cmd_r, cnt_cmd_r),
                'flow_tel_r': (flow_tel_r, cnt_tel_r)
            }

            for flow in flows:
                df = create_dataframe(flow[0])


if __name__ == "__main__":
    main()