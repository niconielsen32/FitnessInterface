clc
clear
close all

%%
% Calculate the pressure from the cylinder. 

piston_radius   = 20 * 10^-3;     % [m]
rod_radus       = 2.5 * 10^-3;    % [m]
pressure        = 6 * 10^5;       % [Pa]

%p[Pa] = F[N] / A[m^2] <=> F = p * A
% The force is different depending on the direction that the air travels
F_piston = pressure * piston_radius^2 * pi; % [N]
F_rod = pressure * (piston_radius^2 * pi - rod_radus^2 * pi); %[N]
disp(['The maximum force put out by the cylinder in push configuration: ', num2str(F_piston), 'N']);
disp(['The maximum force put out by the cylinder in pull configuration: ', num2str(F_rod), 'N']);
disp('-----------------------------------------------------------------------------------------------')

%% Calculate forces on the beam
distance_BA = 400 * 10^-3;  %[m]
distance_AC = 555 * 10^-3;  %[m]


% Sum of moments in point B = 0
pull_force = distance_BA * F_piston / (distance_BA + distance_AC) ;
disp (['The maximum input force: ', num2str(pull_force), ' [N] at distance ', num2str(distance_BA), ' [m]'])

% Maximum bending {omega = (M * c) / I 
syms h b
I_x =@(b,h) 1/12 * b * h^3;
I_y =@(b,h) 1/12 * b^3 * h;
M = distance_BA * F_piston;
c = 15 * 10^-3 ; % [m]
h = 30 * 10^-3 ; % [m]
b = 30 * 10^-3 ; % [m]

omega_x = ( (M * c) / I_x(h, b) ) * 10^-6; %[MPa]
omega_y = ( (M * c) / I_y(h, b) ) * 10^-6; %[MPa]
disp(['The bending moment is calculated to be ', num2str(omega_x), ' [MPa]'])



