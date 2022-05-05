import numpy as np

class ForceCalc:

	def __init__(self, length_to_handle=1, length_to_piston=0.5, update_time=0.5):
		self.old_angle = 0

		self.length_to_handle = length_to_handle
		self.length_to_piston = length_to_piston
		self.update_time = update_time

		self.piston_radius = 20*10**-3

	def calc_power(self, angle, pressure):

		F_piston = pressure*10**5 * self.piston_radius**2 * np.pi
		print("F_piston: ", F_piston)

		force_handle = (self.length_to_piston * F_piston) / self.length_to_handle
		print("Force handle: ", force_handle)

		torque = self.length_to_handle * np.sin(angle) * force_handle
		print("torque: ", torque)
		rotational_speed = (angle - self.old_angle) / self.update_time
		print("rotational: ", rotational_speed)

		power = torque * rotational_speed

		self.old_angle = angle

		return power
