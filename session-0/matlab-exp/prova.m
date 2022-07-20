close all, clear all, clc

pcap_bs = pcapReader("log_2022_07_14_first_bs.pcap", OutputTimestampFormat="microseconds");
pcap_ue = pcapReader("log_2022_07_14_first_ue.pcap", OutputTimestampFormat="microseconds");

packets_bs = pcap_bs.readAll