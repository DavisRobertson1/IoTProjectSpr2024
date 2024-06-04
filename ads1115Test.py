import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

import time

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create a single ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Read the value and print it
i = 0
try:
    while True:
        i+=1
        #try:
            #print(f"ADC Value reading {i}: {chan.value}, Voltage: {chan.voltage}V")
        #except OSError as e:
            #print(f"Failed to read from ADC: {e}")
        print(f"ADC Value reading {i}: {chan.value}, Voltage: {chan.voltage}V")
        time.sleep(2)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
