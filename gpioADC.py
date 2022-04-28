import RPi.GPIO as GPIO

import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import ADC0832 as ADC
# Create an ADC0832 instance
adc = ADC.ADC0832()


potentiometer_channel = 0
pressure_sensor_channel = 1

adc_value_list = []

fig1 = plt.figure("animation 1")
ax = fig1.add_subplot(1, 1, 1)
x1s = []
y1s = []
count_list = []
count = 0


def animate(i, xs, ys):
    # Read temperature (Celsius) from TMP102
    poten_value = adc.read_adc(potentiometer_channel)

    # Add x and y to lists
    global count, count_list
    count_list.append(count)
    count = count + 1
    ys.append(poten_value)

    # Limit x and y lists to 20 items
    count_list = count_list[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(count_list, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Degrees readed from sensor')
    plt.ylabel('Degrees')

# Use try and keyboard exception for cleaning GPIO
try:
    # Main program
    ani = animation.FuncAnimation(fig1, animate, fargs=(x1s, y1s), interval=1000)
    # Sleep for some time - slow down the update rate
    plt.show()

    #potentiometer_value = adc.read_adc(potentiometer_channel)

    #pressure_value = adc.read_adc(pressure_sensor_channel)


    #print("Poten: ", potentiometer_value)
    #print("Pressure: ", pressure_value)



except KeyboardInterrupt:
    print("done")
