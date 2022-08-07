# traffic-analysis

The function of this repo is to collect all logs of the experiments and provide scripts to extract, analyze and visualize data.

## Colosseum csv files

The long file collects all the metrics in append mode, one file for each user (UE). ALl other files are temporary files and can be deleted. Some interesting metrics are the following:

- _dl_buffer [bytes]_ [bytes] is the buffer size in downlink;
- _tx_brate downlink [Mbps]_ is the throughput in downlink;
- _tx_pkts downlink_ is the number of packets exchanged in downlink;
- _rx_brate uplink [Mbps]_ is the same as above;
- _rx_pkts uplink_ is the same as above;
- _ul_sinr_ is the SNR from the user.

See [this webpage](https://www.epochconverter.com/) to convert epoch timestamp and divide the metrics files for each experiment.
