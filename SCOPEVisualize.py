import os, argparse, datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NAMES_DICT = {
    "data/gnd_stl_050.csv": "data/gnd_stl_050",
    "data/gnd_stl_050.csv": "data/gnd_stl_050",
    "data/gnd_stl_075.csv": "data/gnd_stl_075",
    "data/gnd_stl_075.csv": "data/gnd_stl_075",
    "data/gnd_stl_100.csv": "data/gnd_stl_100",
    "data/gnd_stl_100.csv": "data/gnd_stl_100",
    "data/gnd_rot_050.csv": "data/gnd_rot_050",
    "data/gnd_rot_050.csv": "data/gnd_rot_050",
    "data/gnd_rot_075.csv": "data/gnd_rot_075",
    "data/gnd_rot_075.csv": "data/gnd_rot_075",
    "data/gnd_rot_100.csv": "data/gnd_rot_100",
    "data/gnd_rot_100.csv": "data/gnd_rot_100",
    "data/air_stl_050.csv": "data/air_stl_050",
    "data/air_stl_050.csv": "data/air_stl_050"
}
FILES_DICT = {
    "data/gnd_stl_050": "data/gnd_stl_050.csv",
    "data/gnd_stl_050": "data/gnd_stl_050.csv",
    "data/gnd_stl_075": "data/gnd_stl_075.csv",
    "data/gnd_stl_075": "data/gnd_stl_075.csv",
    "data/gnd_stl_100": "data/gnd_stl_100.csv",
    "data/gnd_stl_100": "data/gnd_stl_100.csv",
    "data/gnd_rot_050": "data/gnd_rot_050.csv",
    "data/gnd_rot_050": "data/gnd_rot_050.csv",
    "data/gnd_rot_075": "data/gnd_rot_075.csv",
    "data/gnd_rot_075": "data/gnd_rot_075.csv",
    "data/gnd_rot_100": "data/gnd_rot_100.csv",
    "data/gnd_rot_100": "data/gnd_rot_100.csv",
    "data/air_stl_050": "data/air_stl_050.csv",
    "data/air_stl_050": "data/air_stl_050.csv"
}
COLS_INIT = [
    "Timestamp",  # ms
    "dl_buffer [bytes]",  # bytes
    "tx_brate downlink [Mbps]",  # Mbps
    "tx_pkts downlink",  # number of packets
    "rx_brate uplink [Mbps]",  # Mbps
    "rx_pkts uplink",  # number of packets
    "ul_sinr"
]
COLS_DEF = [
    "Timestamp",  # ms
    "Time_relative",  # ms
    "dl_buffer [bytes]",  # bytes
    "tx_brate downlink [Mbps]",  # Mbps
    "tx_pkts downlink",  # number of packets
    "rx_brate uplink [Mbps]",  # Mbps
    "rx_pkts uplink",  # number of packets
    "ul_sinr"
]
COLS_RENAME_DICT = {
    "Timestamp": "Timestamp",  # ms
    "Time_relative": "Time_relative",  # ms
    "dl_buffer [bytes]": "dl_buffer",  # bytes
    "tx_brate downlink [Mbps]": "tx_brate_downlink",  # Mbps
    "tx_pkts downlink": "tx_pkts_downlink",  # number of packets
    "rx_brate uplink [Mbps]": "rx_brate_uplink",  # Mbps
    "rx_pkts uplink": "rx_pkts_uplink",  # number of packets
    "ul_sinr": "ul_sinr"
}


def read_metrics_csv_and_create_dataframe(file_name, file_path):
    print("Reading " + file_name)
    dataframe = pd.read_csv(file_path, usecols=COLS_INIT)

    # add columns
    dataframe["Time_relative"] = dataframe["Timestamp"] - min(
        dataframe["Timestamp"])

    # reorder columns
    dataframe = dataframe[COLS_DEF]

    # rename columns
    dataframe.rename(columns=COLS_RENAME_DICT, inplace=True)

    return dataframe


def metric_scatterplot(metric_name, dataframe, file_name, file_path):
    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)
    sns.scatterplot(
        x="Time_relative",
        y=metric_name,
        # hue="value",
        # palette="ch:r=-.2,d=.3_r",
        # hue_order=[],
        size=metric_name,
        sizes=(1, 15),
        linewidth=0,
        # ax=ax,
        data=dataframe)
    f.figure.savefig(f"{file_name}_{metric_name}.png")


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

    # save absolute path for the directory where the csv files are saved
    rel_dir = f"./{args.csv_dir}"

    # read .pcapng file and divide flows
    for file in os.listdir(rel_dir):
        if file.endswith('gnd_stl_100.csv'):
            file_path = f"{rel_dir}/{file}"
            file_name = f"{args.csv_dir}/{file}"
            dataframe = read_metrics_csv_and_create_dataframe(
                file_name, file_path)
            for metric in dataframe:
                # TODO: fare delle liste con le varie metriche e dividere per tipi di grafico
                if metric != "Time_relative":
                    metric_scatterplot(metric, dataframe, file_name, file_path)


if __name__ == "__main__":
    main()
