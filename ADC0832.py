#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

ADC_CS  = 11
ADC_CLK = 12 #error, the pin was 13 now corrected to 12 to be consistent with lesson circuit diagram.
ADC_DIO = 13 #error, was 12, now pin 13, to be consistent with lesson circuit diagram.

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location
	GPIO.setup(ADC_CS, GPIO.OUT)
	GPIO.setup(ADC_CLK, GPIO.OUT)

def destroy():
	GPIO.cleanup()

def getResult(channel):     # get ADC result
	GPIO.setup(ADC_DIO, GPIO.OUT)
	GPIO.output(ADC_CLK, 0)
	#time.sleep(0.000002)
	#pull cs low to select chip for input.
	GPIO.output(ADC_CS, 0)
	#send the start bit
	GPIO.output(ADC_DIO, 1)
	GPIO.output(ADC_CLK, 1)
	#time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)
	#time.sleep(0.000002)

	#send SGL / DIF = 1 = Single ended
	GPIO.output(ADC_DIO, 1)
	#time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1)
	#time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)
	#time.sleep(0.000002)
	
	#send the bit to signal which channel 
	#channel 0 
	if channel == 0:
		GPIO.output(ADC_DIO, 0)
		#time.sleep(0.000002)
		GPIO.output(ADC_CLK, 1)
		#time.sleep(0.000002)
	#channel 1 
	elif channel == 1:
		GPIO.output(ADC_DIO, 1)
		#time.sleep(0.000002)
		GPIO.output(ADC_CLK, 1)
		#time.sleep(0.000002)
	
	GPIO.output(ADC_CLK, 0)
	#time.sleep(0.000002)

	#read input off pin
	GPIO.setup(ADC_DIO, GPIO.IN)

	
	GPIO.output(ADC_CLK, 1)
	#time.sleep(0.000002)
		
	dat1 = 0
	for i in range(8):
		GPIO.output(ADC_CLK, 1)
		#time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0)
		dat1 <<= 1	
		if (GPIO.input(ADC_DIO)):		
			dat1 |= 0x1 #GPIO.input(ADC_DIO)
		#time.sleep(0.000002)	
		#time.sleep(0.000002)

		
		
	#dat2 = 0
	#for i in range(0, 8):
	#	dat2 << 1
	#	dat2 = dat2 | GPIO.input(ADC_DIO) #<< i
	#	GPIO.output(ADC_CLK, 1)
	#	time.sleep(0.000002)
	#	GPIO.output(ADC_CLK, 0)
	 #	time.sleep(0.000002)
	
	GPIO.output(ADC_CS, 1)
	GPIO.setup(ADC_DIO, GPIO.OUT)
	return dat1
	#return res
	#if dat1 == dat2:
	#	return dat1
	#else:
	#	return 0

def loop():
	while True:
		res = getResult(0)
		print("x: " + str(res))
		res = getResult(1)
		print("y: " + str(res))
		#print 'res = %d' % res
		time.sleep(0.4)

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
