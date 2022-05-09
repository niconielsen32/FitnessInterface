clc
clear
close all

%REQUIREMENTS: Symbolic Math Toolbox

% This script estimates the following for the exercise machine:
% 1. The minimum width the square beam must have, such that it complies 
% with the factor of safety of two in terms bending stress. No torsion is
% applied to the beam, since all forces are applied on the center axis of
% the beam, so that is ignored.
% 2. That the beam can withstand the worst case stress caused by axial
% loading and the corresponding elongation from the axial loading
% 3. The mimimum diameter the handlebar must have such that it complies 
% with the factor of safety of two in terms of bending and shearing stress.
% 4. The minimum size of the bolts used to mount the bracket connecting the
% handlebar/piston to the beam, such that it can withstand the worst case 
% shearing stress applied to it.

% NOTE - MAYBE DOUBLECHECK WITH INVENTORS OWN CALCULATIONS?
% All of these results have been verified in Inventor, using its own stress
% estimation feature

% CONSTANTS
% Yield strength of the steel is given in the project description as:
omega_y = 235 * 10^6; % [Pa]
% The project description says a factor of safety of teo has to be
% accounted for, which yields the maximum allowed pressure:
omega_all = omega_y/2; % [Pa]
% Radius of inner tube of the piston we are given for the project
piston_radius   = 20 * 10^-3;     % [m]
% Educated guess of the radius of the actual piston. 
% Physical measurement can be taken for a more precise value.
% Not currently used
%rod_radius      = 2.5 * 10^-3;    % [m] 
% Maximum pressure the compressor can deliver according to project
% description
max_pressure = 6 * 10^5;       % [Pa]
% Maximum length the pistion can extrude from the piston housing:
max_piston_stroke = 300 * 10^-3; % [m]
% Lenght of the beam. Remember that a maximum of 1 m of sheet metal can be
% bent.
beam_length = 1000 * 10^-3; % [m]
% Beam width is chosen based on the minimum width calculated in this script
beam_width = 50 *10^-3; % [m]
% Area of the beam with this chosen width is
beam_area = beam_width^2; % [m^2]


% Calculate the largest force the cylinder can produce.
% Pressure is given as: p [Pa] = F [N] / A [m^2] <=> F = p * A
% The force is different depending on the direction that the air travels,
% since the surface of the rod the extrudes from the piston has to be
% negated in one direction, thus the largest pressure will be when the
% chamber not including the rod is pressurised.

F_p = max_pressure * piston_radius^2 * pi; % [N]
disp('-----------------------------------------------------------------------------------------------')
disp(['The maximum force the piston can deliver is: ', num2str(F_p), ' [N]']);

% If the force is needed for the other direction, simply subrtract the area
% of the rod like so:
%F_rod = pressure * (piston_radius^2 * pi - rod_radius^2 * pi); %[N]
%disp(['The maximum force put out by the cylinder in push configuration: ', num2str(F_piston), 'N']);
%disp(['The maximum force put out by the cylinder in pull configuration: ', num2str(F_rod), 'N']);
%disp('-----------------------------------------------------------------------------------------------')

%% Estimate the minimum width of the square beam

% This section relies on a figure that can be found in the figures folder 
% on the git repo. Open it using the drawio web app

% To ensure that the criteria of a factor of safety of two is met it must 
% be calculated for the "worst case scenario", meaning when the biggest 
% moment is acting upon the beam in a point. The position of the brackets 
% mounting the handle/piston to the beam can be changed, but the piston 
% must always be mounted below the handlebars and above the pivot point of 
% the beam. 

% The force contributed by the piston can be broken into an x and y
% composant, but when the piston pushes directly on the beam, meaning when
% the angle between the piston and the beam is exactly 90 degrees, all of
% the force will be applied directly to x-direction of the beam, meaning it
% will contribute only to the bending stress. This angle of 90 degrees is
% obtainable in multiple different mounting positions for the bracket
% connecting the beam and the piston.

% Equivalently, the same is true for the axial stress on the beam, but
% since it is not physically possible for the angle between the piston and
% the beam to be 0 degrees, the "worst case scenario" here becomes when the
% piston is extended its maximum length and mounted as close to the
% rotation point of the bracket connecting the beam to the plate.

% Since the mounting point for the bracket connecting the piston to the
% beam can be changed, an analysis of the largest moments in different 
% mounting points for the piston-bracket is made.
% One would expect the worst case to be when the handlebars are mounted
% furthest away from the center of rotation, since that maximizes the
% length of the beam. One can also make a case for the maximum value of the
% forces in A and C from an analytical standpoint, as if one whishes to
% maximize F_hx and F_bx, AB must be equal to BC.

% Numerical evaluation of which placement of B yields the biggest moment.
% Points A and C are defined as being 0 and 1 m from the rotational point 
% of the beam respectivly since this is determined as the "worst case".
% This yields the distance
d_AC = beam_length; % [m]

% Defining the number of placements of the B-point and X-point
number_of_b_steps = 20;
b_step_size = beam_length / number_of_b_steps;
number_of_x_steps = 20;
x_step_size = beam_length/ number_of_x_steps;

% Defining matrix to store the largest moments for each position of B
% -2 because 0 and 1 are excluded, + 1 because matlab uses 1-indexing
largest_moments = zeros(number_of_b_steps-2+1,2);

index = 1;
for d_AB = b_step_size:b_step_size:0.95
    % Distance AB becomes
    d_BC = 1 - d_AB; % [m]
    % Sum of moments = 0 in point C yields the force in A
    F_bx = F_p * d_BC / d_AC; % [N]
    % Calculating moments in the subsection of the beam AX
    biggest_moment = 0;
    for x_dist = 0:x_step_size:1
        % Sum of moments in X. The moment in B is subtracted when AX > AB
        if x_dist < d_AB
            cur_moment = x_dist * F_bx;
        else
            cur_moment = x_dist * F_bx - (x_dist - d_AB) * F_p; 
        end
        % Save the bigger moment
        if cur_moment > biggest_moment
            biggest_moment = cur_moment;
        end
    end
    % Saving the largest moment for this placement of B
    largest_moments(index,:) = [d_AB biggest_moment];
    index = index + 1;
end

% Visualize data
figure(1)
plot(largest_moments(:,1),largest_moments(:,2))
title('Largest calculated moments as a function of placement of the point B')
xlabel('Distance AB [m]')
ylabel('Largest calculated moment [Nm]')

[largest_moment,Index] = max(largest_moments(:,2));
disp('-----------------------------------------------------------------------------------------------')
disp(['The largest moment found was of size ', num2str(largest_moment), ' [N] and was at the distance AB = ', num2str(largest_moments(Index,1)), ' [m]' ]);

% Now that the biggest moment is known, solving for the minimum width of
% the beam to comply with factor of safety. See lecture 5 slides for
% formulas.
% Symbolic representation of the width
syms W
% The centroid and inertia are defined as:
c = W/2; % [m]
I = W^4/12; % [m^4]
% The equation for bending stress is omega = M*c/I, solving for L yields:
eqn = omega_all == (largest_moment * c) / I;
smallest_beam_width = solve(eqn,W); % [m]

disp('-----------------------------------------------------------------------------------------------')
disp(['The smallest allowable width of the beam is: ', num2str(double(smallest_beam_width(1))*1000), ' [mm]']);

%% (Old version)
% 
% % Constants
% distance_BA = 400 * 10^-3;  %[m]
% distance_AC = 555 * 10^-3;  %[m]
% 
% % Sum of moments in point B = 0
% pull_force = distance_BA * F_piston / (distance_BA + distance_AC) ;
% disp('-----------------------------------------------------------------------------------------------')
% disp (['The maximum input force: ', num2str(pull_force), ' [N] at distance ', num2str(distance_BA), ' [m]'])
% 
% % Bending stress is given as omega = M * c / I 
% I_x =@(b,h) 1/12 * b * h^3;
% I_y =@(b,h) 1/12 * b^3 * h;
% M = distance_BA * F_piston;
% c = 15 * 10^-3 ; % [m]
% h = 30 * 10^-3 ; % [m]
% b = 30 * 10^-3 ; % [m]
% 
% omega_x = ( (M * c) / I_x(h, b) ) * 10^-6; %[MPa]
% omega_y = ( (M * c) / I_y(h, b) ) * 10^-6; %[MPa]
% disp(['The bending moment is calculated to be ', num2str(omega_x), ' [MPa]'])

%% Estimation of axial loading of the beam
% See lecture 4, slide 6-7 for formulas
% Since it is physically impossible to have the angle be 0 degrees, the
% maximum force from the piston will never be fully applied to the axis of
% the beam. However, it it was possible, the axial lodaing stress would be:
% sigma [Pa] = P [N] / A [m^2]
beam_axial_stress = F_p / beam_width^2 * 10^-6; % [MPa]
disp('-----------------------------------------------------------------------------------------------')
disp(['Worst case axial stress on the beam: ', num2str(beam_axial_stress), ' [MPa] which is way below the factor of safety of two of: ', num2str(omega_all*10^-6), ' [MPa]']);
% Now deformation for the max force of the piston is determined.
% The formula is delta = P [N] * L [m] / A [m^2] * E [MPa]
% Modulus of elasticity for the steel we are working with is: (Google)
E = 210 * 10^9; % [GPa]
% Thus yielding the following value for delta
delta = F_p * beam_length / (beam_area * E); % [m]
disp('-----------------------------------------------------------------------------------------------')
disp(['Worst case elongation of the beam: ', num2str(delta*1000), ' [mm]']);
%% Estimation of minimum handlebar diameter

% This assumes a massive rod. Alter the formula for the inertia if using a
% hollow rod by subtracting its inner inertia

% The recepie for calculating the bending moment of the handle can be
% compared to example of the weightlifter in the beginning of lecture 5
% Length of the handle in the CAD-drawing is (disregarding the lip):
handle_lenght = 270 * 10^-3; % [m]
% The width of the extension to which the handle is attached is:
handle_extension_width = 30 * 10^-3; % [m]
% Assuming symmetry and worst case force, each hand yields:
handle_force = F_p / 2; % [N]
% Giving a moment acting on each end of the handle of
handle_moment = handle_force * ((handle_lenght - handle_extension_width) / 2); % [Nm]
% Symbolic variable used to store the radius
syms R
% Centroid and inertia are given as:
handle_centroid = R; % [m]
handle_inertia = pi/4 * R^4; % [m]
% The equation for bending stress is omega = M*c/I, solving for R yields:
handle_radius_eqn = omega_all == (handle_moment * handle_centroid) / handle_inertia;
smallest_handle_radius = solve(handle_radius_eqn,R); % [m]
disp('-----------------------------------------------------------------------------------------------')
disp(['The smallest allowable radius of the handle is: ', num2str(double(smallest_handle_radius(1))*1000), ' [mm]']);

%% Esitmation of minimum bolt size

% Shearing stress is defined as: tau = F / A (see wiki) and from the link 
% below it can be seen that the shear resistance for the absolute smallest 
% bolt is way higher than the worst case force being applied to any of the
% brackets (750 N). Therefore, any bolt should suffice.
% https://eurocodeapplied.com/design/en1993/bolt-design-properties

% Should be good for pop rivetts as well. hear steength is 670 N, so mor
% than one pop rivet is enough, since you can just sum then up