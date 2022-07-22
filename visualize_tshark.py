from cProfile import label
from gettext import dpgettext
import pyshark
import argparse
import os
import time
import statistics
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


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


# def read_pcapng(file_name, file_pathname):

#     print("Reading (with 'tcp' tshark filter) " + file_name + "...")
#     return pyshark.FileCapture(file_pathname, display_filter="tcp")

# def divide_flows(file_name, cap):
#     print("Analyzing " + file_name + "...")

#     # Initialize counters
#     cnt_pckt = 0
#     cnt_nada = 0
#     cnt_ack = 0
#     cnt_cmd_a = 0
#     cnt_tel_a = 0
#     cnt_cmd_r = 0
#     cnt_tel_r = 0

#     # lists to store flows
#     flow_cmd_a = []
#     flow_tel_a = []
#     flow_cmd_r = []
#     flow_tel_r = []
#     flow_nc = []

#     for pckt in cap:
#         cnt_pckt = cnt_pckt + 1  # counter
#         if cnt_pckt % 5000 == 0:
#             print('Analyzed', cnt_pckt, 'so far. Cnt_ack:', cnt_ack)
#         if pckt.tcp.has_field('analysis_ack_rtt'):
#             cnt_ack = cnt_ack + 1

#         # CMD from BS to UE
#         if (str(pckt.ip.src_host) == "172.16.0.1"
#                 and int(pckt.tcp.srcport) == 44584
#                 # and int(pckt.tcp.len) == 44
#             ):
#             cnt_cmd_a = cnt_cmd_a + 1  # counter
#             flow_cmd_a.append(pckt)

#         # Telemetry from BS to UE
#         elif (str(pckt.ip.src_host) == "172.16.0.1"
#               and int(pckt.tcp.srcport) == 44588):
#             cnt_tel_a = cnt_tel_a + 1  # counter
#             flow_tel_a.append(pckt)

#         # CMD_ACK from UE to BS
#         elif (str(pckt.ip.src_host) == "172.16.0.8"
#               and int(pckt.tcp.srcport) == 54166
#               # and int(pckt.tcp.len) == 24
#               ):
#             cnt_cmd_r = cnt_cmd_r + 1  # counter
#             flow_cmd_r.append(pckt)

#         # Telemetry from UE to BS
#         elif (str(pckt.ip.src_host) == "172.16.0.8"
#               and int(pckt.tcp.srcport) == 54168):
#             cnt_tel_r = cnt_tel_r + 1  # counter
#             flow_tel_r.append(pckt)

#         else:
#             cnt_nada = cnt_nada + 1
#             flow_nc.append(pckt)

#     # show table with numbers of packets for each flow
#     print(
#         tabulate([["Flow", "# of packets"], ["Collected packets", cnt_pckt],
#                   ["Non-classified packets", cnt_nada],
#                   ["CMD: BS to UE", cnt_cmd_a], ["TEL: BS to UE", cnt_tel_a],
#                   ["CMD: UE to BS", cnt_cmd_r], ["TEL: UE to BS", cnt_tel_r]]))
#     if (cnt_cmd_a == len(flow_cmd_a) and cnt_cmd_r == len(flow_cmd_r)
#             and cnt_tel_a == len(flow_tel_a) and cnt_tel_r == len(flow_tel_r)):
#         return cnt_pckt, cnt_nada, cnt_cmd_a, cnt_cmd_r, cnt_tel_a, cnt_tel_r, flow_cmd_a, flow_cmd_r, flow_tel_a, flow_tel_r
#     else:
#         exit("Error: counters and flow lengths do not correspond")


def tabulate_packet(pckt):
    print(
        tabulate(
            [["Name", "Class", "Object", "NewClass", "NewObject"],
             [
                 "pckt.highest_layer",
                 type(pckt.highest_layer), pckt.highest_layer, None, None
             ],
             [
                 "pckt.ip.addr",
                 type(pckt.ip.addr), pckt.ip.addr,
                 type(str(pckt.ip.addr)),
                 str(pckt.ip.addr)
             ],
             [
                 "pckt.tcp.srcport",
                 type(pckt.tcp.srcport), pckt.tcp.srcport,
                 type(int(pckt.tcp.srcport)),
                 int(pckt.tcp.srcport)
             ],
             [
                 "pckt.tcp.len",
                 type(pckt.tcp.len), pckt.tcp.len,
                 type(int(pckt.tcp.len)),
                 int(pckt.tcp.len)
             ],
             [
                 "pckt.tcp.analysis_ack_rtt",
                 type(pckt.tcp.analysis_ack_rtt), pckt.tcp.analysis_ack_rtt,
                 type(float(pckt.tcp.analysis_ack_rtt)),
                 float(pckt.tcp.analysis_ack_rtt)
             ]],
            headers='firstrow',
            tablefmt='grid'))


def tcp_table_stats(var: str, flow: list, cnt: int, flow_name: str):
    values = []
    timestamps = []
    for pckt in flow:
        if pckt.tcp.has_field(var):
            values.append(float(pckt.tcp.get_field(var)))
            timestamps.append(
                float(pckt.tcp.get_field('time_relative')) - values[-1])
    avg = statistics.mean(values)
    stdev = statistics.pstdev(values)

    print(
        tabulate([["Flow", "Avg", "StDev"], [flow_name, avg, stdev]],
                 headers='firstrow',
                 tablefmt='grid'))
    return values, timestamps, avg, stdev


def tcp_plot_stats(values: list, timestamps: list, flow_name: str, avg: float,
                   stdev: float):
    my_dpi = 100
    fig = plt.figure(figsize=(1800 / my_dpi, 1000 / my_dpi), dpi=my_dpi)
    plt.scatter(timestamps, values, s=0.5, c='b')
    plt.axhline(y=0.1, color='r', linestyle='-')
    plt.xlabel("Experiment time [s]")
    plt.ylabel("RTT [s]")
    plt.ylim(max(0, avg - 4 * stdev), avg + 4 * stdev)
    plt.grid()
    plt.title(flow_name)
    plt.savefig(flow_name + '.png', dpi=my_dpi)

    # CDF
    df = pd.DataFrame(list(zip(timestamps, values)), columns=['Timestamp', 'Value'])
    plt.figure(figsize=(1800 / my_dpi, 1000 / my_dpi), dpi=my_dpi)
    sns.ecdfplot(data=df, x='Value', label='RTT')
    plt.legend()
    plt.savefig(flow_name + '_cdf.png', dpi=my_dpi)

    # print('\nTime ###########################\n', time)
    # print("\npckt count ", cnt_pckt, " - mav packets ", cnt_cmd, " - non mav packets ",cnt_tel)

    # plt.plot(flow)
    # plt.show()

    # # Normal distribution of flow
    # dis = [0] * 85
    # for pckt in flow:
    #     dis[pckt - 1] = dis[pckt - 1] + 1
    # plt3 = plt.plot(dis)
    # plt.show()


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

    # start = time.time()
    # # read .pcapng file
    # cap = read_pcapng(args.file_name, file_pathname)

    # # divide into the 4 flows of interest
    # (cnt_pckt, cnt_nada, cnt_cmd_a, cnt_cmd_r, cnt_tel_a, cnt_tel_r,
    #  flow_cmd_a, flow_cmd_r, flow_tel_a,
    #  flow_tel_r) = divide_flows(args.file_name, cap)
    # print("Time: ", time.time() - start)

    # plot graphs
    d = {
        'flow_cmd_a': (flow_cmd_a, cnt_cmd_a),
        'flow_tel_a': (flow_tel_a, cnt_tel_a),
        'flow_cmd_r': (flow_cmd_r, cnt_cmd_r),
        'flow_tel_r': (flow_tel_r, cnt_tel_r)
    }
    if args.tcp_vars is not None:
        for var in args.tcp_vars:
            for flow_name in d:
                flow, cnt = d[flow_name]
                values, timestamps, avg, stdev = tcp_table_stats(
                    var, flow, cnt, flow_name)
                tcp_plot_stats(values, timestamps, flow_name, avg, stdev)


if __name__ == "__main__":
    main()