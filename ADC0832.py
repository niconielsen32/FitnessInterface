# A python library to use the ADC0832 analog to digital converter with a Raspberry Pi
# Copyright (C) 2016  Sahithyen Kanaganayagam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import RPi.GPIO as GPIO
import atexit

class ADC0832(object):
    """Functionality to use the analog to digital converter """

    def __init__(self):
        # Initialize pin numbers
        self.csPin = 17
        self.clkPin = 27
        self.doPin = 23
        self.diPin = 24

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
