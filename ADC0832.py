import time
import RPi.GPIO as GPIO
import atexit

class ADC0832(object):
    """Functionality to use the analog to digital converter """

    def __init__(self):
        # Initialize pin numbers
        self.csPin = 8
        self.clkPin = 11
        self.doPin = 10
        self.diPin = 9
        

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.clkPin, GPIO.OUT, initial=GPIO.LOW)

        # Set a cleanup function
        atexit.register(self.cleanup)

    def _getValue(self, sglDif, oddSign):
        timingSecurityOffset = 1.05

        dataMSBFirst = 0
        dataLSBFirst = 0

        ## Select chip
        GPIO.output(self.csPin, GPIO.LOW)

        ## Request data
        GPIO.setup(self.diPin, GPIO.OUT)

        # Start bit
        GPIO.output(self.diPin, GPIO.HIGH)
        time.sleep(0.00025 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.HIGH)
        time.sleep(0.00009 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.LOW)

        # SGL / DIF bit
        GPIO.output(self.diPin, sglDif)
        time.sleep(0.00025 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.HIGH)
        time.sleep(0.00009 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.LOW)

        # ODD / SIGN bit
        GPIO.output(self.diPin, oddSign)
        time.sleep(0.00025 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.HIGH)
        time.sleep(0.00009 * timingSecurityOffset)
        GPIO.output(self.clkPin, GPIO.LOW)

        ## Read data
        GPIO.setup(self.doPin, GPIO.IN)

        # Read MSB Data
        for i in range(8):
            GPIO.output(self.clkPin, GPIO.HIGH)
            time.sleep(0.00009 * timingSecurityOffset)
            GPIO.output(self.clkPin, GPIO.LOW)
            time.sleep(0.0015 * timingSecurityOffset)
            dataMSBFirst = (dataMSBFirst << 1) | GPIO.input(self.doPin)

        # Read LSB Data
        for i in range(8):
            dataLSBFirst = dataLSBFirst | (GPIO.input(self.doPin) << i)
            GPIO.output(self.clkPin, GPIO.HIGH)
            time.sleep(0.00009 * timingSecurityOffset)
            GPIO.output(self.clkPin, GPIO.LOW)
            time.sleep(0.0006 * timingSecurityOffset)

        ## Deselect chip
        GPIO.output(self.csPin, GPIO.HIGH)

        return dataMSBFirst if dataMSBFirst == dataLSBFirst else None

    def read_adc(self, channel):
        return self._getValue(1, channel)

    def read_adc_difference(self, lowChannel):
        return self._getValue(0, lowChannel)

    def cleanup(self):
        GPIO.cleanup()
