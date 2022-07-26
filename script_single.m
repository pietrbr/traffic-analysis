close all
clear all
clc

%%%% ALL STUFF
% VarName = ["slice_prb", "power_multiplier", "scheduling_policy",
% "dl_mcs", "dl_n_samples", "dl_bufferbytes", "tx_brateDownlinkMbps",
% "tx_pktsDownlink", "tx_errorsDownlink", "dl_cqi", "ul_mcs",
% "ul_n_samples", "ul_bufferbytes", "rx_brateUplinkMbps", "rx_pktsUplink",
% "rx_errorsUplink", "ul_rssi", "ul_sinr", "phr", "sum_requested_prbs",
% "sum_granted_prbs", "dl_pmi", "dl_ri", "ul_n", "ul_turbo_iters"];

VarName_all_format = ["Timestamp", "num_ues", "IMSI", "RNTI",...
    "slicing\_enabled", "slice\_id", "slice\_prb", ...
    "power\_multiplier", "scheduling\_policy", ...
    "MCS downlink", "dl\_n\_samples", "Downlink bufferbytes", "Throughput [Mbps]", ...
    "Downlink packets tx", "tx\_errorsDownlink", "CQI", ...
    "MCS uplink", "ul\_n\_samples", "ul\_bufferbytes", ...
    "rx\_brateUplinkMbps", "Uplink packets rx", "Errors", ...
    "ul\_rssi", "SINR uplink", "phr", "Sum of requested PRBs", ...
    "Sum of granted PRBs", "dl\_pmi", "dl\_ri", "ul\_n", ...
    "ul\_turbo\_iters","intf"];

VarName_all = ["Timestamp", "num_ues", "IMSI", "RNTI",...
    "slicing_enabled", "slice_id", "slice_prb", ...
    "power_multiplier", "scheduling_policy", ...
    "dl_mcs", "dl_n_samples", "dl_bufferbytes", "tx_brateDownlinkMbps", ...
    "tx_pktsDownlink", "tx_errorsDownlink", "dl_cqi", ...
    "ul_mcs", "ul_n_samples", "ul_bufferbytes", ...
    "rx_brateUplinkMbps", "rx_pktsUplink", "rx_errorsUplink", ...
    "ul_rssi", "ul_sinr", "phr", "sum_requested_prbs", ...
    "sum_granted_prbs", "dl_pmi", "dl_ri", "ul_n", "ul_turbo_iters","intf"];

%
% x = [slice_prb, ...
%     power_multiplier, scheduling_policy, ...
%     dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
%     ul_mcs, ul_n_samples, ul_bufferbytes, ...
%     rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
%     ul_rssi, ul_sinr, phr, sum_requested_prbs, ...
%     sum_granted_prbs, dl_pmi, dl_ri, ul_n, ul_turbo_iters];

VarName = ["dl\_mcs", ...
    "tx\_brateDownlinkMbps", "dl\_bufferbytes", "dl\_cqi"];
% VarName = ["dl\_mcs", ... % sc
%     "tx\_pktsDownlink", ...
%     "dl\_cqi", "ul\_mcs", ...
%     "rx\_pktsUplink", ...
%     "rx\_errorsUplink", "ul\_sinr", ...
%     "sum\_requested\_prbs"];
% VarName = ["dl\_mcs", "dl\_bufferbytes", ... % gp
%     "tx\_pktsDownlink", ...
%     "dl\_cqi", "ul\_mcs", ...
%     "rx\_pktsUplink", ...
%     "ul\_sinr", ...
%     "sum\_requested\_prbs"];

performance_vars_idx = 1:numel(VarName_all);
performance_vars_idx =  performance_vars_idx(~cellfun(@isempty,regexp(VarName_all,strjoin(VarName,'|'))));

% 
z = [];

folder_path_real_world = './data_rw';
folder_path_colosseum_1 = './data_col_1';
folder_path_colosseum_2 = './data_col_2';
folder_path_colosseum_3 = './data_col_3';
folder_path_colosseum = './data_col_all';

% folders = {folder_path_real_world, folder_path_colosseum};

%% CHANGE FLAGS HERE!
flags = [0];
flags = [1];
flags = [2];
flags = [3];
flags = [4];

%% 
all_folders = {folder_path_real_world, folder_path_colosseum_1, folder_path_colosseum_2, folder_path_colosseum_3, folder_path_colosseum};
folder_path = all_folders(flags+1); % +1 to use the correct indeces

wildcard = '/*.csv';
 
main_folder = char(folder_path);
filenames = dir(strcat(main_folder,wildcard));

for i = 1 : numel(filenames)
    
    [Timestamp, num_ues, IMSI, RNTI, VarName5,...
        slicing_enabled, slice_id, slice_prb, ...
        power_multiplier, scheduling_policy, VarName11, ...
        dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
        VarName19, ul_mcs, ul_n_samples, ul_bufferbytes, ...
        rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
        ul_rssi, ul_sinr, phr, VarName29, sum_requested_prbs, ...
        sum_granted_prbs, VarName32, dl_pmi, dl_ri, ul_n, ul_turbo_iters ...
        ] = importfile(fullfile(filenames(i).folder,filenames(i).name));
    
    x = [Timestamp, num_ues, IMSI, RNTI,...
        slicing_enabled, slice_id, slice_prb, ...
        power_multiplier, scheduling_policy, ...
        dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
        ul_mcs, ul_n_samples, ul_bufferbytes, ...
        rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
        ul_rssi, ul_sinr, phr, sum_requested_prbs, ...
        sum_granted_prbs, dl_pmi, dl_ri, ul_n, ul_turbo_iters];
    
%     x = [x, flags(j).*ones(size(x,1),1), conf_setups(k).*ones(size(x,1),1)];
    x(x(:,VarName_all == "dl_cqi")<1,:) = []; % remove entries that are ill-defined
    x(x(:,VarName_all == "dl_mcs")<1,:) = []; % remove entries that are ill-defined
    x(x(:,VarName_all == "ul_mcs")<1,:) = []; % remove entries that are ill-defined
    x(x(:,VarName_all == "ul_cqi")<1,:) = []; % remove entries that are ill-defined
    x(x(:,find(VarName_all == "tx_brateDownlinkMbps"))==0,:) = []; % remove entries that are ill-defined
    z = [z; x];
    
end


%% compare 2 examples

conf_test_id = 5;
num_cols = size(z,2);

% z_test = z(z(:,num_cols)==conf_setups(conf_test_id),:);

z_test = z;

figure(1)
imagesc(corr(z(:,performance_vars_idx)))
colormap(jet)
colorbar
caxis([-1 1])
set(gca, 'XTick', 1:numel(VarName)); % center x-axis ticks on bins
set(gca, 'YTick', 1:numel(VarName)); % center y-axis ticks on bins
set(gca,'XTickLabel',VarName_all_format(performance_vars_idx));
set(gca,'YTickLabel',VarName_all_format(performance_vars_idx));
savefig('scope_matlab_plots/imagesc.fig')

groups = cell(size(z_test,1),1);
% groups(z_test(:,num_cols-1)==1) = {'Colosseum'};
groups(z_test(:,num_cols-1)==0) = {'Real world'};
groups(z_test(:,num_cols-1)==1) = {'Colosseum 1 uav'};
groups(z_test(:,num_cols-1)==2) = {'Colosseum 3 uav'};
groups(z_test(:,num_cols-1)==3) = {'Colosseum 1 uav + 3 ue'};
groups(z_test(:,num_cols-1)==4) = {'Colosseum'};

figure(2)
gplotmatrix(z_test(:,performance_vars_idx),[],groups,'br','..',[],'on',[],VarName_all_format(:,performance_vars_idx),VarName_all_format(:,performance_vars_idx))
legend('Colosseum')
savefig('scope_matlab_plots/gplotmatrix.fig')

%%

metric1 = 16; % CQI
metric2 = 10; % MCS

figure(3)
s = scatterhist(z_test(:,metric1),z_test(:,metric2),'Group',groups,...
    'Kernel','overlay',...
    'Style','bar',...
    'Marker','ox',...
    'MarkerSize',6,...
    'Location','NorthEast',...
    'Direction','out')
grid on
ylabel(VarName_all_format(metric2))
xlabel(VarName_all_format(metric1))
legend('Colosseum')
savefig('scope_matlab_plots/scatterhist.fig')
