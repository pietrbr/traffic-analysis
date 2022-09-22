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
