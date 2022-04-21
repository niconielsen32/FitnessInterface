import RPi.GPIO as GPIO
import ADC0832
import time

 
potentiometer_channel = 0
pressure_sensor_channel = 1

adc_value_list = []
# Use try and keyboard exception for cleaning GPIO
try:
    # Main program
    
    while True:
        
        potentiometer_value = ADC0832.getResult(potentiometer_channel)
        
        pressure_value = ADC0832.getResult(pressure_sensor_channel)
       
        
        print("Poten: ", potentiometer_value)
        print("Pressure: ", pressure_value)
        
        # Sleep for some time - slow down the update rate
        time.sleep(0.5)
            
         
