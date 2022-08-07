#!/bin/python3
import os, argparse
import pyshark, argparse, os
from tabulate import tabulate
import pandas as pd

PORTS_DICT = {
    "data/gnd_stl_050_bs.pcapng": [44584, 44588, 54166, 54168],
    "data/gnd_stl_050_ue.pcapng": [44584, 44588, 54166, 54168],
    "data/gnd_stl_075_bs.pcapng": [44594, 44596, 54174, 54176],
    "data/gnd_stl_075_ue.pcapng": [44594, 44596, 54174, 54176],
    "data/gnd_stl_100_bs.pcapng": [44590, 44592, 54170, 54172],
    "data/gnd_stl_100_ue.pcapng": [44590, 44592, 54170, 54172],
    "data/gnd_rot_050_bs.pcapng": [33154, 33158, 60524, 60526],
    "data/gnd_rot_050_ue.pcapng": [33154, 33158, 60524, 60526],
    "data/gnd_rot_075_bs.pcapng": [33160, 33162, 60528, 60530],
    "data/gnd_rot_075_ue.pcapng": [33160, 33162, 60528, 60530],
    "data/gnd_rot_100_bs.pcapng": [33166, 33168, 60534, 60536],
    "data/gnd_rot_100_ue.pcapng": [33166, 33168, 60534, 60536],
    "data/air_stl_050_bs.pcapng": [33170, 33172, 60538, 60540],
    "data/air_stl_050_ue.pcapng": [33170, 33172, 60538, 60540]
}
NAMES_DICT = {
    "data/gnd_stl_050_bs.pcapng": "data/gnd_stl_050_bs",
    "data/gnd_stl_050_ue.pcapng": "data/gnd_stl_050_ue",
    "data/gnd_stl_075_bs.pcapng": "data/gnd_stl_075_bs",
    "data/gnd_stl_075_ue.pcapng": "data/gnd_stl_075_ue",
    "data/gnd_stl_100_bs.pcapng": "data/gnd_stl_100_bs",
    "data/gnd_stl_100_ue.pcapng": "data/gnd_stl_100_ue",
    "data/gnd_rot_050_bs.pcapng": "data/gnd_rot_050_bs",
    "data/gnd_rot_050_ue.pcapng": "data/gnd_rot_050_ue",
    "data/gnd_rot_075_bs.pcapng": "data/gnd_rot_075_bs",
    "data/gnd_rot_075_ue.pcapng": "data/gnd_rot_075_ue",
    "data/gnd_rot_100_bs.pcapng": "data/gnd_rot_100_bs",
    "data/gnd_rot_100_ue.pcapng": "data/gnd_rot_100_ue",
    "data/air_stl_050_bs.pcapng": "data/air_stl_050_bs",
    "data/air_stl_050_ue.pcapng": "data/air_stl_050_ue"
}
FILES_DICT = {
    "data/gnd_stl_050_bs": "data/gnd_stl_050_bs.pcapng",
    "data/gnd_stl_050_ue": "data/gnd_stl_050_ue.pcapng",
    "data/gnd_stl_075_bs": "data/gnd_stl_075_bs.pcapng",
    "data/gnd_stl_075_ue": "data/gnd_stl_075_ue.pcapng",
    "data/gnd_stl_100_bs": "data/gnd_stl_100_bs.pcapng",
    "data/gnd_stl_100_ue": "data/gnd_stl_100_ue.pcapng",
    "data/gnd_rot_050_bs": "data/gnd_rot_050_bs.pcapng",
    "data/gnd_rot_050_ue": "data/gnd_rot_050_ue.pcapng",
    "data/gnd_rot_075_bs": "data/gnd_rot_075_bs.pcapng",
    "data/gnd_rot_075_ue": "data/gnd_rot_075_ue.pcapng",
    "data/gnd_rot_100_bs": "data/gnd_rot_100_bs.pcapng",
    "data/gnd_rot_100_ue": "data/gnd_rot_100_ue.pcapng",
    "data/air_stl_050_bs": "data/air_stl_050_bs.pcapng",
    "data/air_stl_050_ue": "data/air_stl_050_ue.pcapng"
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

    print_flows_table(len(flow_cmd_a), len(flow_tel_a), len(flow_cmd_r),
                      len(flow_tel_r))

    # TODO: evaluate if it is convenient to compute the counter of the number of packets... it may take time
    return len(flow_cmd_a), len(flow_tel_a), len(flow_cmd_r), len(
        flow_tel_r), flow_cmd_a, flow_tel_a, flow_cmd_r, flow_tel_r


def print_flows_table(len_flow_cmd_a, len_flow_tel_a, len_flow_cmd_r,
                      len_flow_tel_r):
    """show table with numbers of packets for each flow"""
    print(
        tabulate([["Flow", "# of packets"], ["CMD: BS to UE", len_flow_cmd_a],
                  ["CMD: UE to BS", len_flow_tel_a],
                  ["TEL: BS to UE", len_flow_cmd_r],
                  ["TEL: UE to BS", len_flow_tel_r],
                  [
                      "Collected packets (presumed)", len_flow_cmd_a +
                      len_flow_tel_a + len_flow_cmd_r + len_flow_tel_r
                  ], ["Non-classified packets", "N/A"]]))


def create_dataframe(flow):
    Number = []
    Timestamp = []
    Time_relative = []
    Time_IDT = []
    Tcp_len = []
    Tcp_flag_syn = []
    Tcp_flag_ack = []
    Tcp_ack = []
    Tcp_RTT = []
    Tcp_initial_RTT = []
    Retransmission = []
    Ack_lost_segment = []
    Duplicate_ack = []

    for pckt in flow:
        Number.append(int(pckt.number))
        Timestamp.append(float(pckt.sniff_timestamp))
        Time_relative.append(float(pckt.tcp.get_field("time_relative")))
        Time_IDT.append(float(pckt.tcp.get_field("time_delta")))
        Tcp_len.append(float(pckt.tcp.get_field("len")))
        Tcp_flag_syn.append(bool(int(pckt.tcp.flags_syn)))
        Tcp_flag_ack.append(bool(int(pckt.tcp.flags_ack)))
        Tcp_ack.append(bool(int(pckt.tcp.ack)))
        if Tcp_flag_ack[-1] is True:
            if pckt.tcp.has_field("analysis_ack_rtt"):
                Tcp_RTT.append(float(pckt.tcp.get_field("analysis_ack_rtt")))
            else:
                Tcp_RTT.append(None)
            if pckt.tcp.has_field("analysis_initial_rtt"):
                Tcp_initial_RTT.append(
                    float(pckt.tcp.get_field("analysis_initial_rtt")))
            else:
                Tcp_initial_RTT.append(None)
            Retransmission.append(
                pckt.tcp.has_field("analysis_retransmission")
                or pckt.tcp.has_field("analysis_fast_retransmission"))
            Ack_lost_segment.append(
                pckt.tcp.has_field("analysis_ack_lost_segment"))
            Duplicate_ack.append(pckt.tcp.get_field("duplicate_ack"))
        elif Tcp_flag_ack[-1] is False:
            Tcp_RTT.append(None)
            Tcp_initial_RTT.append(None)
            Retransmission.append(None)
            Ack_lost_segment.append(None)
            Duplicate_ack.append(None)

        # ##### DEBUG
        # if (len(Number) == len(Timestamp) == len(Time_relative) ==
        #         len(Time_IDT) == len(Tcp_len) == len(Tcp_flag_syn) ==
        #         len(Tcp_flag_ack) == len(Tcp_ack) == len(Tcp_RTT) ==
        #         len(Tcp_initial_RTT) == len(Retransmission) ==
        #         len(Ack_lost_segment) == len(Duplicate_ack)):
        #     print("True: same len")
        #     print(
        #         pd.DataFrame(zip(Number, Timestamp, Time_relative, Time_IDT,
        #                          Tcp_len, Tcp_flag_syn, Tcp_flag_ack, Tcp_ack,
        #                          Tcp_RTT, Tcp_initial_RTT, Retransmission,
        #                          Ack_lost_segment, Duplicate_ack),
        #                      columns=[
        #                          "Number", "Timestamp", "Time_relative",
        #                          "Time_IDT", "Tcp_len", "Tcp_flag_syn",
        #                          "Tcp_flag_ack", "Tcp_ack", "Tcp_RTT",
        #                          "Tcp_initial_RTT", "Lost_segment",
        #                          "Ack_lost_segment", "Duplicate_ack"
        #                      ]).iloc[-1])  #debug
        # else:
        #     print("False: different len")
        # ##### END DEBUG

    dataframe = pd.DataFrame(zip(Number, Timestamp, Time_relative, Time_IDT,
                                 Tcp_len, Tcp_flag_syn, Tcp_flag_ack, Tcp_ack,
                                 Tcp_RTT, Tcp_initial_RTT, Retransmission,
                                 Ack_lost_segment, Duplicate_ack),
                             columns=[
                                 "Number", "Timestamp", "Time_relative",
                                 "Time_IDT", "Tcp_len", "Tcp_flag_syn",
                                 "Tcp_flag_ack", "Tcp_ack", "Tcp_RTT",
                                 "Tcp_initial_RTT", "Lost_segment",
                                 "Ack_lost_segment", "Duplicate_ack"
                             ])
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
        default='data',
        help=
        'Relative path of the directory; supposed to accept an argument like "data".'
    )
    args = parser.parse_args()

    # save absolute path for the directory where the pcapng files are saved
    rel_dir = f"./{args.pcapng_dir}"

    # read .pcapng file and divide flows
    for file in os.listdir(rel_dir):
        if file.endswith('gnd_stl_100_bs.pcapng'):
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