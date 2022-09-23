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
    "slicing_enabled", "slice\_id", "slice\_prb", ...
    "power_multiplier", "scheduling\_policy", ...
    "MCS", "dl\_n\_samples", "dl\_bufferbytes", "Throughput [Mbps]", ...
    "tx\_pktsDownlink", "tx\_errorsDownlink", "CQI", ...
    "ul\_mcs", "ul\_n\_samples", "ul\_bufferbytes", ...
    "rx\_brateUplinkMbps", "rx\_pktsUplink", "Errors", ...
    "ul\_rssi", "ul\_sinr", "phr", "sum\_requested_prbs", ...
    "sum\_granted\_prbs", "dl\_pmi", "dl\_ri", "ul\_n", ...
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

VarName = ["dl_mcs", ...
    "tx_brateDownlinkMbps", "dl_bufferbytes", "dl_cqi"];

% Interesting varaibles given by Salvo
VarName = ["dl\_mcs", "dl\_n\_samples", "dl\_bufferbytes", ...
    "tx\_brateDownlinkMbps", "tx\_pktsDownlink", ...
    "tx\_errorsDownlink", "dl\_cqi", ...
    "ul\_mcs", "ul\_n\_samples", "ul\_bufferbytes", ...
    "rx\_brateUplinkMbps", "rx\_pktsUplink", "rx\_errorsUplink", ...
    "ul\_rssi", "ul\_sinr", "sum\_requested\_prbs", ...
    "sum\_granted\_prbs"];

performance_vars_idx = 1:numel(VarName_all);
performance_vars_idx =  performance_vars_idx(~cellfun(@isempty,regexp(VarName_all,strjoin(VarName,'|'))));

conf_setups = [1]; % rbs

z = [];

for k = 1 : numel(conf_setups)
    
    conf_id = k-1;
    
    folder_path = strcat('./data');
    
    folders = {folder_path};
    flags = [0;1];
    wildcard = '/*.csv';
    
    for j = 1 : numel(folders)
        
        main_folder = char(folders(j));
        filenames = dir(strcat(main_folder,wildcard));
        
        for i = 1 : numel(filenames)
            
            [Timestamp, num_ues, IMSI, RNTI, VarName5,...
                slicing_enabled, slice_id, slice_prb, ...
                power_multiplier, scheduling_policy, VarName11, ...
                dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
                VarName19, ul_mcs, ul_n_samples, ul_bufferbytes, ...
                rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
                ul_rssi, ul_sinr, phr, VarName29, sum_requested_prbs, ...
                sum_granted_prbs, VarName32, dl_pmi, dl_ri, ul_n, ul_turbo_iters] = importfile(fullfile(filenames(i).folder,filenames(i).name));
            
            
            x = [Timestamp, num_ues, IMSI, RNTI,...
                slicing_enabled, slice_id, slice_prb, ...
                power_multiplier, scheduling_policy, ...
                dl_mcs, dl_n_samples, dl_bufferbytes, tx_brateDownlinkMbps, tx_pktsDownlink, tx_errorsDownlink, dl_cqi, ...
                ul_mcs, ul_n_samples, ul_bufferbytes, ...
                rx_brateUplinkMbps, rx_pktsUplink, rx_errorsUplink, ...
                ul_rssi, ul_sinr, phr, sum_requested_prbs, ...
                sum_granted_prbs, dl_pmi, dl_ri, ul_n, ul_turbo_iters];
            
            x = [x, flags(j).*ones(size(x,1),1), conf_setups(k).*ones(size(x,1),1)];
            x(x(:,find(VarName == "dl_cqi"))==0,:) = []; % remove entries that are ill-defined
            x(x(:,find(VarName == "dl_mcs"))==0,:) = []; % remove entries that are ill-defined
            x(x(:,find(VarName == "ul_mcs"))==0,:) = []; % remove entries that are ill-defined
            x(x(:,find(VarName == "ul_cqi"))==0,:) = []; % remove entries that are ill-defined

            z = [z; x];
            
        end
    end
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

groups = cell(size(z_test,1),1);
groups(z_test(:,num_cols-1)==1) = {'Real world'};
groups(z_test(:,num_cols-1)==0) = {'Colosseum'};

figure(2)
gplotmatrix(z_test(:,performance_vars_idx),[],groups,'br','..',[],'on',[],VarName_all_format(:,performance_vars_idx),VarName_all_format(:,performance_vars_idx))

%%

metric1 = 16;
metric2 = 10;

figure(3)
s = scatterhist(z_test(:,metric1),z_test(:,metric2),'Group',groups,...
    'Kernel','overlay',...
    'Style','bar',...
    'Marker','ox',...
    'MarkerSize',6,...
    'Location','NorthEast',...
    'Direction','out');
grid on
ylabel(VarName_all_format(metric2))
xlabel(VarName_all_format(metric1))
% legend('Jamming ON','Jamming OFF')
