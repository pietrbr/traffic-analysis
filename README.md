# traffic-analysis

This repository collects all data collected in the experiments and provide scripts to extract, analyze and visualize it.

## Scripts description

| Python script name           | Description                                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| main.py                      | This was supposed to be a script used as a launcher. Currently discontinued.                                 |
| prova.py                     | This is a script used for tests.                                                                             |
| SCOPEmetricsReadVisualize.py | This is currently substituted by the matlab scripts.                                                         |
| pcapngRead.py                | THis script should read the pcapng files, extract the data,  and save the data structures into pickle files. |
| pcapngVisualize.py           | THis script should read the pickle files and plot stuff.                                                     |
| analyze_data_tshark.py       | This was supposed to be a script used as a launcher. Currently discontinued.                                 |
| tsharkCaptureAnalyzer.py     | This was supposed to be a script used as a launcher for the pcapng Read and Visualize scripts (?).           |

| Matlab script name  | Description                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------- |
| counter.m           | This file is used to count the number of packets in the data chunk analyzed.             |
| importfile.m        | This function is used to import data from the csv.                                       |
| salvo_original.m    | This is the original code given by Salvo.                                                |
| script_comaprison.m | This is the definitive code, where it is possible to run different kinds of comparisons. |
| script_single.m     | This is a previous and simplified version of script_comparison.m                         |

## Colosseum csv files

The long file collects all the metrics in append mode, one file for each user (UE). ALl other files are temporary files and can be deleted. Some interesting metrics are the following:

- _dl_buffer [bytes]_ [bytes] is the buffer size in downlink;
- _tx_brate downlink [Mbps]_ is the throughput in downlink;
- _tx_pkts downlink_ is the number of packets exchanged in downlink;
- _rx_brate uplink [Mbps]_ is the same as above;
- _rx_pkts uplink_ is the same as above;
- _ul_sinr_ is the SNR from the user.

See [this webpage](https://www.epochconverter.com/) to convert epoch timestamp and divide the metrics files for each experiment.
