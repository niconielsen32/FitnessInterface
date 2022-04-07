import RPi.GPIO as GPIO

import time


# SPI Pins
PIN_CLK = 11
PIN_MOSI = 10
PIN_MISO = 9
PIN_CS = 8


#global variables
ADCvalue = 0


def init_GPIO():
    # Init GPIO pins
    GPIO.setmode(GPIO.BCM)
    
    # Spi pins Init
    GPIO.setup(PIN_CLK, GPIO.OUT)
    GPIO.setup(PIN_MISO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_MOSI, GPIO.OUT)
    GPIO.setup(PIN_CS, GPIO.OUT)


   
# Read SPI data from ADC
def recvBits(numBits, clkPin, misoPin):
    #Receives arbitrary number of bits
    retVal = 0
    
    for bit in range(numBits):
        # Pulse clock pin 
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)
        
        # Read 1 data bit in
        if GPIO.input(misoPin):
            retVal |= 0x1
        
        # Advance input to next bit
        retVal <<= 1
    
    # Divide by two to drop the NULL bit
    return (retVal/2)


def readAdc(csPin, clkPin, misoPin, mosiPin, csPin):
        
    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(csPin, GPIO.HIGH)
    
    # Start the read with both clock and chip select low
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.HIGH)
    
    adcValue = recvBits(10, clkPin, misoPin)
    
    # Set chip select high to end the read
    GPIO.output(csPin, GPIO.HIGH)
  
    return round(adcValue)

 
adcValueList = []
# Use try and keyboard exception for cleaning GPIO
try:
    # Main program
    print("Initializing GPIO and window")
    init_GPIO()
    
    while True:
        
        # Channel 0
        potentiometer_value = readAdc(0, PIN_CLK, PIN_MISO, PIN_MOSI, PIN_CS)
        # Channel 1 - might need to just change the pins on raspberry to get the 2 channels instead.
        # GPIO 7 and 8 and then SPI setup pins - Outputs on 7 and 8
        pressure_value = readAdc(0, PIN_CLK, PIN_MISO, PIN_MOSI, PIN_CS)
        
        print("Poten: ", potentiometer_value)
        print("Pressure: ", pressure_value)
        # Sleep for some time - slow down the update rate
        time.sleep(0.5)
            
         
            
           
        
        
except KeyboardInterrupt:
    # Clean/reset GPIO pins before program terminates
    GPIO.cleanup()
    
