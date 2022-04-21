import RPi.GPIO as GPIO

import time

import ADC0832 as ADC
# Create an ADC0832 instance
adc = ADC.ADC0832()

 
potentiometer_channel = 0
pressure_sensor_channel = 1

adc_value_list = []
# Use try and keyboard exception for cleaning GPIO
try:
    # Main program
    
    while True:
        
        potentiometer_value = adc.read_adc(potentiometer_channel)
        
        pressure_value = adc.read_adc(pressure_sensor_channel)
       
        
        print("Poten: ", potentiometer_value)
        print("Pressure: ", pressure_value)
        
        # Sleep for some time - slow down the update rate
        time.sleep(0.5)
            
         
