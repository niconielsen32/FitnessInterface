import RPi.GPIO as GPIO

import time


# SPI Pins
PIN_CLK = 11
PIN_MOSI = 10
PIN_MISO = 9
PIN_CE0 = 8
PIN_CE1 = 7


#global variables
ADCvalue = 0


def init_GPIO():
    # Init GPIO pins
    GPIO.setmode(GPIO.BCM)
    
    # Spi pins Init
    GPIO.setup(PIN_CLK, GPIO.OUT)
    GPIO.setup(PIN_MISO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_MOSI, GPIO.OUT)
    GPIO.setup(PIN_CE0, GPIO.OUT)
    GPIO.setup(PIN_CE1, GPIO.OUT)


   
# Read SPI data from ADC
def receive_bits(number_of_bits, clk_pin, miso_pin):
    #Receives arbitrary number of bits
    return_value = 0
    
    for bit in range(number_of_bits):
        # Pulse clock pin 
        GPIO.output(clk_pin, GPIO.HIGH)
        GPIO.output(clk_pin, GPIO.LOW)
        
        # Read 1 data bit in
        if GPIO.input(miso_pin):
            return_value |= 0x1
        
        # Advance input to next bit
        return_value <<= 1
    
    # Divide by two to drop the NULL bit
    return (return_value/2)


def read_adc_value(cs_pin, clk_pin, miso_pin, mosi_pin):
        
    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(cs_pin, GPIO.HIGH)
    
    # Start the read with both clock and chip select low
    GPIO.output(cs_pin, GPIO.LOW)
    GPIO.output(clk_pin, GPIO.HIGH)
    
    adc_value = receive_bits(number_of_bits=10, clk_pin, miso_pin)
    
    # Set chip select high to end the read
    GPIO.output(cs_pin, GPIO.HIGH)
  
    return round(adc_value)

 
adc_value_list = []
# Use try and keyboard exception for cleaning GPIO
try:
    # Main program
    print("Initializing GPIO and window")
    init_GPIO()
    
    while True:
        
        # Channel 0
        potentiometer_value = read_adc_value(PIN_CE0, PIN_CLK, PIN_MISO, PIN_MOSI)
        # Channel 1 - might need to just change the pins on raspberry to get the 2 channels instead.
        # GPIO 7 and 8 and then SPI setup pins - Outputs on 7 and 8
        pressure_value = read_adc_value(PIN_CE1, PIN_CLK, PIN_MISO, PIN_MOSI)
        
        print("Poten: ", potentiometer_value)
        print("Pressure: ", pressure_value)
        # Sleep for some time - slow down the update rate
        time.sleep(0.5)
            
         
            
           
        
        
except KeyboardInterrupt:
    # Clean/reset GPIO pins before program terminates
    GPIO.cleanup()
    
