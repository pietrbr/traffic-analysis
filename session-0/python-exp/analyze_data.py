import pyshark
import os
import statistics
import matplotlib.pyplot as plt
from tabulate import tabulate


def daje():
    file_dir = os.path.dirname(os.path.realpath(__file__))

    # list to store files
    flow_cmd_a = []
    flow_cmd_r = []
    flow_tel_a = []
    flow_tel_r = []

    # Variables
    # mavlink_hl_string = "MAVLINK_PROTO"
    hl_string = "TCP"
    cnt_tel = 0
    cnt_cmd = 0
    cnt_pckt = 0
    cnt_nada = 0
    time = 0

    ## debug section
    # cap = list(pyshark.FileCapture('/home/pietro/Documents/ditg/wireshark-data/capture-armed-1.pcapng'))
    # time = cap[-1].sniff_time - cap[0].sniff_time
    # time_span_s = time.seconds + time.microseconds / 10**6
    # print(time, time_span_s)
    # quit()

    # Iterate directory
    for file in os.listdir(file_dir):
        # check only .pcapng files
        if file.endswith('.pcapng'):
            # cap = pyshark.FileCapture(
            #     file_dir + '/' + file,
            #     'lua_script:/home/pietro/.local/lib/wireshark/plugins/mavlink_2_common.lua',
            #     display_filter='mavlink_proto')
            cap = pyshark.FileCapture(file_dir + '/' + file,
                                      display_filter="tcp")

            # # compute time span
            # time_span = cap[-1].sniff_time - cap[0].sniff_time
            # time = time + time_span.seconds + time_span.microseconds / 10**6

            print("Analyzing ", file, "...")
            for pckt in cap:
                cnt_pckt = cnt_pckt + 1  # counter

                # # if TCP
                # if pckt.highest_layer == hl_string:

                # print(
                #     tabulate(
                #         [["Name", "Class", "Object", "NewClass", "NewObject"],
                #          [
                #              "pckt.highest_layer",
                #              type(pckt.highest_layer), pckt.highest_layer,
                #              None, None
                #          ],
                #          [
                #              "pckt.ip.addr",
                #              type(pckt.ip.addr), pckt.ip.addr,
                #              type(str(pckt.ip.addr)),
                #              str(pckt.ip.addr)
                #          ],
                #          [
                #              "pckt.tcp.srcport",
                #              type(pckt.tcp.srcport), pckt.tcp.srcport,
                #              type(int(pckt.tcp.srcport)),
                #              int(pckt.tcp.srcport)
                #          ],
                #          [
                #              "pckt.tcp.len",
                #              type(pckt.tcp.len), pckt.tcp.len,
                #              type(int(pckt.tcp.len)),
                #              int(pckt.tcp.len)
                #          ]]))

                # if it is a command from BS
                if (str(pckt.ip.src_host) == "172.16.0.1"
                        and int(pckt.tcp.srcport) == 48094
                        and int(pckt.tcp.len) == 44):
                    cnt_cmd = cnt_cmd + 1  # counter
                    flow_cmd_a.append(int(pckt.tcp.len))

                # if it is a command from UE
                elif (str(pckt.ip.src_host) == "172.16.0.8"
                      and int(pckt.tcp.srcport) == 37574
                      and int(pckt.tcp.len) == 24):
                    cnt_cmd = cnt_cmd + 1  # counter
                    flow_cmd_r.append(int(pckt.tcp.len))

                # else if is telemetry from BS
                elif (str(pckt.ip.src_host) == "172.16.0.1"
                      and int(pckt.tcp.srcport) == 48096):
                    cnt_cmd = cnt_cmd + 1  # counter
                    flow_cmd_a.append(int(pckt.tcp.len))

                # else if is telemetry from UE
                elif (str(pckt.ip.src_host) == "172.16.0.8"
                      and int(pckt.tcp.srcport) == 37576):
                    cnt_cmd = cnt_cmd + 1  # counter
                    flow_cmd_r.append(int(pckt.tcp.len))

                else:
                    cnt_nada = cnt_nada + 1

    # Results
    print("\ncnt_pckt", cnt_pckt, "\ncnt_nada: ", cnt_nada, "\ncnt_cmd: ",
          cnt_cmd, "\ncnt_tel: ", cnt_tel)
    avg_cmd_a = statistics.mean(flow_cmd_a)
    avg_cmd_r = statistics.mean(flow_cmd_r)
    avg_tel_a = statistics.mean(flow_tel_a)
    avg_tel_r = statistics.mean(flow_tel_r)
    stdev_cmd_a = statistics.pstdev(flow_cmd_a)
    stdev_cmd_r = statistics.pstdev(flow_cmd_r)
    stdev_tel_a = statistics.pstdev(flow_tel_a)
    stdev_tel_r = statistics.pstdev(flow_tel_r)

    table1 = [["Flow", "Avg", "StDev"], [flow_cmd_a, avg_cmd_a, stdev_cmd_a],
              [flow_cmd_r, avg_cmd_r, stdev_cmd_r],
              [flow_tel_a, avg_tel_a, stdev_tel_a],
              [flow_tel_r, avg_tel_r, stdev_tel_r]]
    print(tabulate(table1, headers='firstrow', tablefmt='grid'))

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
    daje()


if __name__ == "__main__":
    main()