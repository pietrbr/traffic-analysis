clear all
close all
clc

%%%% ALL STUFF
% VarName = ["slice_prb", "power_multiplier", "scheduling_policy",
% "dl_mcs", "dl_n_samples", "dl_bufferbytes", "tx_brateDownlinkMbps",
% "tx_pktsDownlink", "tx_errorsDownlink", "dl_cqi", "ul_mcs",
% "ul_n_samples", "ul_bufferbytes", "rx_brateUplinkMbps", "rx_pktsUplink",
% "rx_errorsUplink", "ul_rssi", "ul_sinr", "phr", "sum_requested_prbs",
% "sum_granted_prbs", "dl_pmi", "dl_ri", "ul_n", "ul_turbo_iters"];

VarName_all_format = ["Timestamp", "num_ues", "IMSI", "RNTI",...
    "slicing_enabled", "slice_id", "slice_prb", ...
    "power_multiplier", "scheduling_policy", ...
    "MCS", "dl_n_samples", "dl_bufferbytes", "Throughput [Mbps]", "tx_pktsDownlink", "tx_errorsDownlink", "CQI", ...
    "ul_mcs", "ul_n_samples", "ul_bufferbytes", ...
    "rx_brateUplinkMbps", "rx_pktsUplink", "Errors", ...
    "ul_rssi", "ul_sinr", "phr", "sum_requested_prbs", ...
    "sum_granted_prbs", "dl_pmi", "dl_ri", "ul_n", "ul_turbo_iters","intf"];

VarName_all = ["Timestamp", "num_ues", "IMSI", "RNTI",...
    "slicing_enabled", "slice_id", "slice_prb", ...
    "power_multiplier", "scheduling_policy", ...
    "dl_mcs", "dl_n_samples", "dl_bufferbytes", "tx_brateDownlinkMbps", "tx_pktsDownlink", "tx_errorsDownlink", "dl_cqi", ...
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

performance_vars_idx = 1:numel(VarName_all);
performance_vars_idx =  performance_vars_idx(~cellfun(@isempty,regexp(VarName_all,strjoin(VarName,'|'))));

conf_setups = [0 2 4 6 8]; % [50 44 38 32 26] rbs

z = [];

for k = 1 : numel(conf_setups)
    
    conf_id = k-1;
    
    folder_path_no_wifi = strcat('/home/salvo/Documents/DRL_coexistence/training_data/no_wifi/tr',num2str(conf_id));
    folder_path_wifi = strcat('/home/salvo/Documents/DRL_coexistence/training_data/with_wifi/tr',num2str(conf_id));
    
    folders = {folder_path_no_wifi, folder_path_wifi};
    flags = [0;1];
    wildcard = '/*/*/*/*/*_metrics.csv';
    
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
groups(z_test(:,num_cols-1)==1) = {'Jamming ON'};
groups(z_test(:,num_cols-1)==0) = {'Jamming OFF'};

figure(2)
gplotmatrix(z_test(:,performance_vars_idx),[],groups,'br','..',[],'on',[],VarName_all_format(:,performance_vars_idx),VarName_all_format(:,performance_vars_idx))

%%

metric1 = 4;
metric2 = 1;

figure(3)
s = scatterhist(z_test(:,metric1),z_test(:,metric2),'Group',groups,...
    'Kernel','overlay',...
    'Style','bar',...
    'Marker','ox',...
    'MarkerSize',6,...
    'Location','NorthEast',...
    'Direction','out')
grid on
ylabel(VarName(metric2))
xlabel(VarName(metric1))
% legend('Jamming ON','Jamming OFF')