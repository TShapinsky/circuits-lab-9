%% Importing CSVs 

part1 = csvread("exp2_part1_v2=3.499.csv",1);
part2 = csvread("exp2_part2_v2=3.499.csv",1);
part3 = csvread("exp2_part2_v2=3.499.csv",1);

%% Separating out variables 

Vdm = part1(:,1); 
Vout = part1(:,2);

Vout2 = part2(:,1); 
Iout2 = part2(:,2);

Vout3 = part3(:,1); 
Iout3 = part3(:,2); 

%% Generating theoretical lines 

poly1 = polyfit(Vdm(463:545),Vout(463:545),1); 
poly2 = polyfit(Vout2(15:471),Iout2(15:471),1); 
poly3 = polyfit(Vout3(15:471), Iout3(15:471),1); 

theor1 = poly1(1)*Vdm(463:545)+ poly1(2);
theor2 = poly2(1)*Vout2(10:471) + poly2(2);
theor3 = poly3(1)*Vout3(10:471) + poly3(2);

%% Display slopes

slope1 = poly1(1);
slope2 = poly2(1);
slope3 = poly3(1);

disp(slope1);
disp(slope2);
disp(slope3);

%% Plot 

figure
plot(Vdm, Vout, '.'); 
grid on;
hold on;
plot(Vdm(463:545), theor1, 'r', 'LineWidth', 2);
xlabel("Vdm (Volts)");
ylabel("Vout (Volts)");
title("Vdm vs Vout");
set(gcf,'color','w');
xlim([-0.04 0.04]);
legend('measured','theoretical')

figure 
plot(Vout2, Iout2, '.');
grid on;
hold on;
plot(Vout2(10:471), theor2, 'r', 'LineWidth', 2);
xlabel("Vout (Volts)"); 
ylabel("Iout (Amps)"); 
title("Current-Voltage Characteristic when Vdm = 0");
set(gcf,'color','w');
legend('measured','theoretical')

figure 
plot(Vout3, Iout3, '.');
grid on;
hold on;
plot(Vout3(10:471), theor3, 'r', 'LineWidth', 2);
xlabel("Vdm (Volts)"); %Is this right?
ylabel("Iout (Amps)");
title("Current-Voltage Characteristic when Vout = 3.5V");
set(gcf,'color','w');
legend('measured','theoretical')

