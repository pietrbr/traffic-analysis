import pyshark
import os

import time
start_time = time.time()

# PARAMETERS
mavlink_hl_string = "MAVLINK_PROTO"
file_dir = os.path.dirname(os.path.realpath(__file__))

# VARIABLES
idt = 0
# forth (BS to UE)
fa = open(file_dir + "/background_traffic_size_a.txt", "w")
ga = open(file_dir + "/background_traffic_time_a.txt", "w")
ta0 = 0
ta1 = 0

# back (UE to BS)
fr = open(file_dir + "/background_traffic_size_r.txt", "w")
gr = open(file_dir + "/background_traffic_time_r.txt", "w")
tr0 = 0
tr1 = 0

for file in os.listdir(file_dir):
    # check only .pcapng files
    if file.endswith('background_traffic_p.pcapng'):
        print("Analyzing ", file, "...")
        cap = pyshark.FileCapture(
            file_dir + '/' + file,
            'lua_script:/home/pietro/.local/lib/wireshark/plugins/mavlink_2_common.lua',
            display_filter='mavlink_proto')

        cnt = 0
        cnta = 0
        cntr = 0
        for pckt in cap:
            if pckt.highest_layer == mavlink_hl_string:
                cnt = cnt + 1
                # forth
                if int(pckt.tcp.dstport) == 5760:
                    cnta = cnta + 1
                    # size
                    fa.write(str(pckt.tcp.len) + "\n")
                    # inter-departure time
                    ta0 = ta1
                    ta1 = pckt.sniff_time
                    if ta0 != 0:
                        idt = ta1 - ta0
                        ga.write(str(idt.microseconds / 1000) + "\n")
                    else:
                        pass

                # back
                elif int(pckt.tcp.srcport) == 5760:
                    cntr = cntr + 1
                    # size
                    fr.write(str(pckt.tcp.len) + "\n")
                    # inter-departure time
                    tr0 = tr1
                    tr1 = pckt.sniff_time
                    if tr0 != 0:
                        idt = tr1 - tr0
                        gr.write(str(idt.microseconds / 1000) + "\n")
                    else:
                        pass

                # What?
                else:
                    # print(pckt)
                    pass
        print("Counters for file", str(file) + ": ", cnt, cnta, cntr)

fa.close()
ga.close()
fr.close()
gr.close()

print("--- %s seconds ---" % (time.time() - start_time))