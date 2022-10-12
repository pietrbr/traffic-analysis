from SCOPEmetricsReadVisualize import *
from pcapngRead import *
from pcapngVisualize import *
import re


PCAPNG_DF_COLS = [
    'Number', 'Timestamp', 'Time_relative', 'Time_IDT', 'Tcp_len',
    'Tcp_flag_syn', 'Tcp_flag_ack', 'Tcp_ack', 'Tcp_RTT', 'Tcp_initial_RTT',
    'Retransmission', 'Ack_lost_segment', 'Duplicate_ack', 'location', 'state',
    'distance', 'side', 'cmd', 'flow'
]


def pcapng_plotter():
    pkl_dir = "data"
    rel_dir = "./" + pkl_dir
    # read .pkl file and divide flows
    pkl_files = [file for file in os.listdir(rel_dir) if file.endswith('.pkl')]
    dfs = {}

    for file in pkl_files:
        dfs[file] = pd.read_pickle(rel_dir + "/" + file)
        loc, state, dist, side, _, cmd, flow, _ = re.split("_|\.",
                                                           file,
                                                           maxsplit=7)
        dfs[file]['location'] = loc
        dfs[file]['state'] = state
        dfs[file]['distance'] = dist
        dfs[file]['side'] = side
        dfs[file]['cmd'] = cmd
        dfs[file]['flow'] = flow

    df = pd.concat([dfs[file] for file in dfs], ignore_index=True)
    df = df.drop(
        [
            # "Number", "Timestamp", "Tcp_flag_syn", 'Tcp_flag_ack', 'Tcp_ack', 'location', 'state', 'side', 'cmd', 'flow'
            'Number',
            'Timestamp',
            'Tcp_len',
            'Tcp_flag_syn',
            'Tcp_flag_ack',
            'Tcp_ack',
            'Tcp_RTT',
            'Tcp_initial_RTT',
            # 'Retransmission',
            'Ack_lost_segment',
            'Duplicate_ack',
            'location',
            'state',
            'side',
            'cmd',
            'flow'
        ],
        axis=1)
    pcapng_scatterplotmatrix(df, hue="distance", graph_name="distance")


def main():
    ## SCOPE PLOTS
    # scope_plotter()

    ## TSHARK PLOTS
    pcapng_plotter()


if __name__ == "__main__":
    main()
