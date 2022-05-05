
old_angle = 0
new_angle = 0

length_to_handle = 1
update_time = 0.5

piston_radius = 20**-3

length_to_piston = 0.5

F_piston = pressure * piston_radius**2 * np.pi

force_handle = (length_to_piston * F_piston) / length_to_handle

torque = length_to_handle * np.sin(new_angle) * force_handle
rotational_speed = (new_angle - old_angle) / update_time

power = torque * rotational_speed
