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
    "session-2/tshark_bs/tshark_log_2022_07_26_20_01_29.pcapng":
    None,
    "session-2/tshark_bs/tshark_log_2022_07_26_20_22_51.pcapng":
    None
}
FILES_DICT = {
    "session-0/a":
    "session-0/log_2022_07_14_first_bs.pcap",
    "session-0/b":
    "session-0/log_2022_07_14_first_ue.pcap",
    "session-1/tshark_bs/05.0m":
    "session-1/tshark_bs/tshark_log_2022_07_20_19_34_17.pcapng",
    "session-1/tshark_bs/10.0m":
    "session-1/tshark_bs/tshark_log_2022_07_20_19_59_22.pcapng",
    "session-1/tshark_bs/07.5m":
    "session-1/tshark_bs/tshark_log_2022_07_20_20_21_20.pcapng",
    "session-1/tshark_ue/05.0m":
    "session-1/tshark_ue/tshark_log_2022_07_20_19_31_27.pcapng",
    "session-1/tshark_ue/10.0m":
    "session-1/tshark_ue/tshark_log_2022_07_20_19_59_25.pcapng",
    "session-1/tshark_ue/07.5m":
    "session-1/tshark_ue/tshark_log_2022_07_20_20_21_17.pcapng",
    "session-2/tshark_bs/05.0m":
    "session-2/tshark_bs/tshark_log_2022_07_26_20_01_29.pcapng",
    "session-2/tshark_bs/10.0m":
    "session-2/tshark_bs/tshark_log_2022_07_26_20_22_51.pcapng"
}
NAMES_DICT = {
    "session-0/log_2022_07_14_first_bs.pcap":
    "session-0/a",
    "session-0/log_2022_07_14_first_ue.pcap":
    "session-0/b",
    "session-1/tshark_bs/tshark_log_2022_07_20_19_34_17.pcapng":
    "session-1/tshark_bs/05.0m",
    "session-1/tshark_bs/tshark_log_2022_07_20_19_59_22.pcapng":
    "session-1/tshark_bs/10.0m",
    "session-1/tshark_bs/tshark_log_2022_07_20_20_21_20.pcapng":
    "session-1/tshark_bs/07.5m",
    "session-1/tshark_ue/tshark_log_2022_07_20_19_31_27.pcapng":
    "session-1/tshark_ue/05.0m",
    "session-1/tshark_ue/tshark_log_2022_07_20_19_59_25.pcapng":
    "session-1/tshark_ue/10.0m",
    "session-1/tshark_ue/tshark_log_2022_07_20_20_21_17.pcapng":
    "session-1/tshark_ue/07.5m",
    "session-2/tshark_bs/tshark_log_2022_07_26_20_01_29.pcapng":
    "session-2/tshark_bs/05.0m",
    "session-2/tshark_bs/tshark_log_2022_07_26_20_22_51.pcapng":
    "session-2/tshark_bs/10.0m"
}


def read_pcapng_and_divide_flows(file_name, file_path):
    """
    file_name: name of the file
    file_path: realtive path of the file, including the name of the file
    """

    # lists to store the four flows
    flow_cmd_a = []
    flow_tel_a = []
    flow_cmd_r = []
    flow_tel_r = []

    ports = PORTS_DICT[file_name]

    # CMD_a
    print("Reading " + file_name + " for flow_cmd_a")
    flow_cmd_a = pyshark.FileCapture(
        file_path,
        display_filter=
        f"(ip.src_host ==172.16.0.1 && tcp.srcport=={ports[0]}) || (ip.dst_host ==172.16.0.1 && tcp.dstport=={ports[0]})"
    )
    flow_cmd_a.load_packets()

    # TEL_a
    print("Reading " + file_name + " for flow_tel_a")
    flow_tel_a = pyshark.FileCapture(
        file_path,
        display_filter=
        f"(ip.src_host ==172.16.0.1 && tcp.srcport=={ports[1]}) || (ip.dst_host ==172.16.0.1 && tcp.dstport=={ports[1]})"
    )
    flow_tel_a.load_packets()

    # CMD_r
    print("Reading " + file_name + " for flow_cmd_r")
    flow_cmd_r = pyshark.FileCapture(
        file_path,
        display_filter=
        f"(ip.src_host ==172.16.0.8 && tcp.srcport=={ports[2]}) || (ip.dst_host ==172.16.0.8 && tcp.dstport=={ports[2]})"
    )
    flow_cmd_r.load_packets()

    # TEL_r
    print("Reading " + file_name + " for flow_tel_r")
    flow_tel_r = pyshark.FileCapture(
        file_path,
        display_filter=
        f"(ip.src_host ==172.16.0.8 && tcp.srcport=={ports[3]}) || (ip.dst_host ==172.16.0.8 && tcp.dstport=={ports[3]})"
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

    # TODO: evaluate if it is convenient to compute the counter of the number of packets... it may take time
    return len(flow_cmd_a), len(flow_tel_a), len(flow_cmd_r), len(
        flow_tel_r), flow_cmd_a, flow_tel_a, flow_cmd_r, flow_tel_r


def create_dataframe(flow):
    Timestamp = [float(pckt.sniff_timestamp) for pckt in flow]
    dataframe = pd.DataFrame(zip(Timestamp), columns=["Timestamp"])
    return dataframe


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description=
        'Read pcapng files, filter and divide packets into flows, and save the flows to pickle files.'
    )
    parser.add_argument(
        'pcapng_dir',
        metavar='pcapng_dir',
        type=str,
        nargs='?',
        help=
        'Relative path of the directory; supposed to accept an argument like "session-1/tshark_bs".'
    )
    args = parser.parse_args()

    # save ablsoulte path for the directory where the pcapng files are saved
    rel_dir = f"./{args.pcapng_dir}"

    # read .pcapng file and divide flows
    for file in os.listdir(rel_dir):
        if file.endswith('.pcapng'):
            file_path = f"{rel_dir}/{file}"
            file_name = f"{args.pcapng_dir}/{file}"
            (cnt_cmd_a, cnt_tel_a, cnt_cmd_r, cnt_tel_r, flow_cmd_a,
             flow_tel_a, flow_cmd_r,
             flow_tel_r) = read_pcapng_and_divide_flows(file_name, file_path)
            flows = {
                'flow_cmd_a': (flow_cmd_a, cnt_cmd_a),
                'flow_tel_a': (flow_tel_a, cnt_tel_a),
                'flow_cmd_r': (flow_cmd_r, cnt_cmd_r),
                'flow_tel_r': (flow_tel_r, cnt_tel_r)
            }

            for flow in flows:
                df = create_dataframe(flows[flow][0])
                pickle_name = f"{NAMES_DICT[file_name]}_{flow}.pkl"
                df.to_pickle(pickle_name)


if __name__ == "__main__":
    main()