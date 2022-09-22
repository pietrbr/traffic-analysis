import os, argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NAMES_DICT = {
    "data/gnd_stl_050.csv": "data/scope_figs/gnd_stl_050",
    "data/gnd_stl_050.csv": "data/scope_figs/gnd_stl_050",
    "data/gnd_stl_075.csv": "data/scope_figs/gnd_stl_075",
    "data/gnd_stl_075.csv": "data/scope_figs/gnd_stl_075",
    "data/gnd_stl_100.csv": "data/scope_figs/gnd_stl_100",
    "data/gnd_stl_100.csv": "data/scope_figs/gnd_stl_100",
    "data/gnd_rot_050.csv": "data/scope_figs/gnd_rot_050",
    "data/gnd_rot_050.csv": "data/scope_figs/gnd_rot_050",
    "data/gnd_rot_075.csv": "data/scope_figs/gnd_rot_075",
    "data/gnd_rot_075.csv": "data/scope_figs/gnd_rot_075",
    "data/gnd_rot_100.csv": "data/scope_figs/gnd_rot_100",
    "data/gnd_rot_100.csv": "data/scope_figs/gnd_rot_100",
    "data/air_stl_050.csv": "data/scope_figs/air_stl_050",
    "data/air_stl_050.csv": "data/scope_figs/air_stl_050"
}

# unused
# FILES_DICT = {
#     "data/gnd_stl_050": "data/gnd_stl_050.csv",
#     "data/gnd_stl_050": "data/gnd_stl_050.csv",
#     "data/gnd_stl_075": "data/gnd_stl_075.csv",
#     "data/gnd_stl_075": "data/gnd_stl_075.csv",
#     "data/gnd_stl_100": "data/gnd_stl_100.csv",
#     "data/gnd_stl_100": "data/gnd_stl_100.csv",
#     "data/gnd_rot_050": "data/gnd_rot_050.csv",
#     "data/gnd_rot_050": "data/gnd_rot_050.csv",
#     "data/gnd_rot_075": "data/gnd_rot_075.csv",
#     "data/gnd_rot_075": "data/gnd_rot_075.csv",
#     "data/gnd_rot_100": "data/gnd_rot_100.csv",
#     "data/gnd_rot_100": "data/gnd_rot_100.csv",
#     "data/air_stl_050": "data/air_stl_050.csv",
#     "data/air_stl_050": "data/air_stl_050.csv"
# }

# to select the columns to extract from the csv file
COLS_EXTRACT = [
    "Timestamp",  # ms
    "dl_buffer [bytes]",  # bytes
    "tx_brate downlink [Mbps]",  # Mbps
    "tx_pkts downlink",  # number of packets
    "rx_brate uplink [Mbps]",  # Mbps
    "rx_pkts uplink",  # number of packets
    "ul_sinr"
]

# to order the columns of the dataframe
COLS_ORDER = [
    "Timestamp",  # ms
    "Time_relative",  # ms
    "dl_buffer [bytes]",  # bytes
    "tx_brate downlink [Mbps]",  # Mbps
    "tx_pkts downlink",  # number of packets
    "rx_brate uplink [Mbps]",  # Mbps
    "rx_pkts uplink",  # number of packets
    "ul_sinr"
]

#COLS_RENAME = [
#     "Timestamp (epoch time) [ms]",  # ms
#     "Relative time [s]",  # ms
#     "Downlink buffer size [bytes]",  # bytes
#     "tx_brate_downlink",  # Mbps
#     "Downlink transmitted packets",  # number of packets
#     "rx_brate_uplink",  # Mbps
#     "Uplink transmitted packets",  # number of packets
#     "SiNR (uplink)"
# ]

# to rename the columns of the dataframe
COLS_RENAME_DICT = {
    "Timestamp": "Timestamp (epoch time) [ms]",  # ms
    "Time_relative": "Relative time [s]",  # ms
    "dl_buffer [bytes]": "Downlink buffer size [bytes]",  # bytes
    "tx_brate downlink [Mbps]": "tx_brate_downlink",  # Mbps
    "tx_pkts downlink": "Downlink transmitted packets",  # number of packets
    "rx_brate uplink [Mbps]": "rx_brate_uplink",  # Mbps
    "rx_pkts uplink": "Uplink transmitted packets",  # number of packets
    "ul_sinr": "SiNR (uplink)"
}

# to save files with the columns' names without spaces
COLS_NAME_TO_SAVE_FILES = {
    "Timestamp (epoch time) [ms]": "epochtime",
    "Relative time [s]": "time",
    "Downlink buffer size [bytes]": "dl_buffer_size",
    "tx_brate_downlink": "tx_brate_downlink",
    "Downlink transmitted packets": "dl_transmitted_packets",
    "rx_brate_uplink": "rx_brate_uplink",
    "Uplink transmitted packets": "ul_transmitted_packets",
    "SiNR (uplink)": "SiNR"
}


def read_metrics_csv_and_create_dataframe(file_name, file_path):
    print("Reading " + file_name)
    dataframe = pd.read_csv(file_path, usecols=COLS_EXTRACT)

    # add column for relative time in [ms]
    dataframe["Time_relative"] = (dataframe["Timestamp"] -
                                  min(dataframe["Timestamp"])) / 1000

    # reorder columns
    dataframe = dataframe[COLS_ORDER]

    # rename columns
    dataframe.rename(columns=COLS_RENAME_DICT, inplace=True)

    return dataframe


def metric_scatterplot(metric_name, dataframe, file_name):
    # TODO: requires hue to select different kind of flows (distance, kind of flow, etc.);
    sns.set_theme(style="whitegrid")
    # sns.set_theme(style="ticks")
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=False, bottom=False)

    sns.scatterplot(
        x=COLS_RENAME_DICT["Time_relative"],
        y=metric_name,
        # hue="value",
        # palette="ch:r=-.2,d=.3_r",
        # hue_order=[],
        size=metric_name,
        sizes=(1, 15),
        linewidth=0,
        ax=ax,
        data=dataframe)
    f.figure.savefig(
        f"{NAMES_DICT[file_name]}_{COLS_NAME_TO_SAVE_FILES[metric_name]}.png")


def metric_scatterplotmatrix(dataframe, hue="", graph_name=""):
    if graph_name == "":
        graph_name = hue

    sns.set_theme(style="ticks")
    f, ax = plt.subplots(figsize=(12, 12))
    # sns.despine(f, left=True, bottom=True)

    sns.pairplot(dataframe, hue=hue)
    f.figure.savefig(f"scatterplot_{graph_name}.png")


# def scope_huge_dataframe(df):
#     for file in df:
#         df[file]
#         # dataframe = pd
#     return dataframe

# def scope_plotter():
#     csv_dir = "data"
#     rel_dir = "./" + csv_dir
#     # read .pcapng file and divide flows
#     csv_files = [file for file in os.listdir(rel_dir) if file.endswith('.csv')]
#     df = {}

#     for file in csv_files:
#         file_path = f"{rel_dir}/{file}"
#         file_name = f"{csv_dir}/{file}"
#         df[file] = read_metrics_csv_and_create_dataframe(file_name, file_path)

#     dataframe = scope_huge_dataframe(df)

#     metric_scatterplotmatrix(dataframe, hue="", graph_name="")
#     plt.close()


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Read csv SCOPE metrics files and visualize the data.')
    parser.add_argument(
        'csv_dir',
        metavar='csv_dir',
        type=str,
        nargs='?',
        default='data',
        help=
        'Relative path of the directory; supposed to accept an argument like "data".'
    )
    args = parser.parse_args()

    # save absolute path for the directory where the csv files are
    # saved
    rel_dir = f"./{args.csv_dir}"

    # read all .csv files in the directory
    
    for file in [file for file in os.listdir(rel_dir) if file.endswith(".csv")]:
    # These two following lines should be equivalent to the previous one
    # for file in os.listdir(rel_dir):
    #     if file.endswith('.csv'):
        file_path = f"{rel_dir}/{file}"
        file_name = f"{args.csv_dir}/{file}"
        dataframe = read_metrics_csv_and_create_dataframe(
            file_name, file_path)
        for metric in dataframe:
            # TODO: fare delle liste con le varie metriche e dividere per tipi di grafico
            if metric != COLS_RENAME_DICT[
                    "Time_relative"] and metric != COLS_RENAME_DICT[
                        "Timestamp"]:
                metric_scatterplot(metric, dataframe, file_name)
                plt.close()


if __name__ == "__main__":
    main()
