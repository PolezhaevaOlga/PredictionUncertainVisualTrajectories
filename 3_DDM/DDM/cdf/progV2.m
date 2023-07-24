close all
%cd('C:\0_Disque_Isa\M-A')

S=dir('*.csv');
L = length(S);

min_scale = -1
max_scale = 1;

x_new = linspace(min_scale, max_scale, 30);

%for i=1:10

FILENAME=S(20).name;


mat = readmatrix(FILENAME);
x_emp = mat(:,1);
y_emp =mat(:,2);
x_adj = mat(:,3);
y_adj =mat(:,4);
figure('Position', [10 10 800 700]) % create a figure of size 8x7 inches
axes('FontName','Times New Roman') % set font to Times New Roman
%plot(x_emp,y_emp,'ko','MarkerSize',7)
scatter(x_emp,y_emp,50,'o','MarkerEdgeColor', 'k', 'MarkerFaceColor', 'w','linewidth',1)
hold on
plot(x_adj, y_adj,'k--','LineWidth', 2)
legend('empirical','predicted',FontSize=17,FontName = 'Times New Roman',Location='northwest')
xlabel('Reaction time (s)',FontSize=20, FontName = 'Times New Roman')
%box off
%xline(0)
xlim([-1.5 1.5])
set(gca, 'XAxisLocation', 'origin', 'YAxisLocation', 'origin')
print('-dpng','-r300','cdf_ex.jpg')
% extraire les parties correspondant aux valeurs positives des x

ind_emp_pos = find(x_emp>0);
x_emp_pos = x_emp(ind_emp_pos);
y_emp_pos = y_emp(ind_emp_pos);

ind_adj_pos = find(x_adj>0);
x_adj_pos = x_adj(ind_adj_pos);
y_adj_pos = y_adj(ind_adj_pos);

% on cherche les valeurs dans y_adj qui correspondant aux x_emp_pos
y_interp_adj = interp1(x_adj_pos,y_adj_pos, x_emp_pos);

%plot(x_emp_pos,y_emp_pos,'r.', x_emp_pos, y_interp_adj, 'k.') 

% val_min = min(A(:,1));
% val_max = max(A(:,1));


%plot(y_emp_pos, y_interp_adj,'.')
new_mat = [x_emp_pos,y_emp_pos, y_interp_adj];

%new_FILENAME=[FILENAME(1:length(FILENAME)-4) '.txt']
%save(new_FILENAME, 'new_mat', '-ascii', '-tabs')

%end

