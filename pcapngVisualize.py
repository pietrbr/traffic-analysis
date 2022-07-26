#!/bin/python3
import statistics
import pyshark, argparse, os
from tabulate import tabulate
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


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
    df = pd.DataFrame(list(zip(timestamps, values)),
                      columns=['Timestamp', 'Value'])
    plt.figure(figsize=(1800 / my_dpi, 1000 / my_dpi), dpi=my_dpi)
    sns.ecdfplot(data=df, x='Value', label='RTT')
    plt.legend()
    plt.savefig(flow_name + '_cdf.png', dpi=my_dpi)
