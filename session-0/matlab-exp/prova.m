close all, clear all, clc

CAPTURE_FILE = 'log_2022_07_14_first_bs.pcapng';

dissector = {'tcp.len','tcp.dstport'};

read_filter = '';

pcap_bs = pcapReader()


