% 1659039871831-1659039026081
close all
clear all
clc

% Counters
j = 0;
pckt_n = 0;
time = 0;

folder = './data_rw';
% folder = './data_col_1';
% folder = './data_col_2';
% folder = './data_col_3';

wildcard = '/*.csv';
    
    
filenames = dir(strcat(folder,wildcard));

for i = 1 : numel(filenames)

    [Timestamp, num_ues, IMSI, RNTI, VarName5,...
        slicing_enabled, slice_id, slice_prb, ...
        power_multiplier, scheduling_policy, VarName11, ...
        dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, ...
        tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
        VarName19, ul_mcs, ul_n_samples, ul_bufferbytes, ...
        rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
        ul_rssi, ul_sinr, phr, VarName29, sum_requested_prbs, ...
        sum_granted_prbs, VarName32, dl_pmi, dl_ri, ul_n, ul_turbo_iters] = ...
        importfile(fullfile(filenames(i).folder,filenames(i).name));

    pckt_n = pckt_n + length(Timestamp);
    time = time + (Timestamp(end) - Timestamp(1));
end

% t = datetime(time, 'ConvertFrom', 'posixtime');

fprintf("Folder %s\n", folder)
fprintf("Number of packets: %d\n", pckt_n)
fprintf("Total time: %d\n", time)

% To convert to relative time
% https://www.unixtimestamp.com/index.php