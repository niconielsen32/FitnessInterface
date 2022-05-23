import RPi.GPIO as GPIO

import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from ForceCalc import ForceCalc

import ADC0832 as ADC
# Create an ADC0832 instance
adc = ADC.ADC0832()


potentiometer_channel = 1
pressure_sensor_channel = 0

adc_value_list = []

fig1 = plt.figure("animation 1")
ax = fig1.add_subplot(1, 1, 1)
x1s = []
y1s = []
count_list = []
count = 0

power_calc = ForceCalc()


old_time = 0.0
cur_time = 0.0

angle_ref = 0
angle_offset = 50.32

over_all_distance_traveled_by_piston = 0

def get_pressure_abs(voltage):
    angle = ((voltage - 0.5) / 0.04) * 0.0689475729 
    if angle < 0.0:
        return 0.0

    return angle

def get_pressure_seagled(voltage):
    pressure = (((voltage - 0.4766)/0.3783))

    return pressure


def get_angle(angle_voltage_per):
    return (angle_voltage_per + 8.333) / 0.389



def animate(i, xs, ys):
    global old_time, angle_ref, over_all_distance_traveled_by_piston
    potentiometer_value = adc.read_adc(potentiometer_channel)
    cur_time = time.perf_counter()
    angle_voltage_per = (potentiometer_value / 255) * 100
    cur_angle = get_angle(angle_voltage_per)
    angle = (cur_angle - angle_ref)*-1 + angle_offset

    pressure_value = adc.read_adc(pressure_sensor_channel)
    voltage = (pressure_value / 255) * 5
    pressure = get_pressure_seagled(voltage)

    cur_power, cur_change_in_piston_length = power_calc.calc_power(angle, pressure, (cur_time - old_time))
    
    over_all_distance_traveled_by_piston = over_all_distance_traveled_by_piston + abs(cur_change_in_piston_length)

    # Add x and y to lists
    global count, count_list
    count_list.append(count)
    count = count + 1
    ys.append(cur_power)


    old_time = cur_time

    # Limit x and y lists to 20 items
    count_list = count_list[-200:]
    ys = ys[-200:]

    # Draw x and y lists
    ax.clear()
    ax.plot(count_list, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Current power')
    plt.ylabel('Power [W]')

# Use try and keyboard exception for cleaning GPIO
potentiometer_value = adc.read_adc(potentiometer_channel)
voltage = (potentiometer_value / 255) * 100
angle_ref = get_angle(voltage)
old_time = time.perf_counter()
# Main program
training_start_time = time.perf_counter()
ani = animation.FuncAnimation(fig1, animate, fargs=(x1s, y1s), interval=10)
# Sleep for some time - slow down the update rate
plt.show()
training_end_time = time.perf_counter()

pressure_value = adc.read_adc(pressure_sensor_channel)
voltage = (pressure_value / 255) * 5
pressure = get_pressure_seagled(voltage)
f_piston = power_calc.get_f_piston(pressure)
print(over_all_distance_traveled_by_piston)
print("Power over the whole exercise: ", (over_all_distance_traveled_by_piston / (training_end_time - training_start_time)) * f_piston)