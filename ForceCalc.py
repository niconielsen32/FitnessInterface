from cmath import sqrt
import numpy as np

class ForceCalc:

	def __init__(self, length_to_handle=0.96, length_to_piston=0.45):
		self.length_to_piston = 0.39
		self.beam_to_piston = 0.695

		self.piston_radius = 20*10**-3
		self.old_piston_length = 0.481

	def calc_power(self, angle, pressure, time):
		piston_length = self.length_to_piston**2 + self.beam_to_piston**2 - 2*self.length_to_piston*self.beam_to_piston*np.cos(np.deg2rad(angle))
		piston_length = np.sqrt(piston_length)
		F_piston = pressure*(10**5) * self.piston_radius**2 * np.pi

		speed = (piston_length - self.old_piston_length) / time

		power = F_piston * speed

		piston_change = piston_length - self.old_piston_length
		self.old_piston_length = piston_length

		return power, piston_change


	def get_f_piston(self, pressure):
		F_piston = pressure*(10**5) * self.piston_radius**2 * np.pi
		return F_piston