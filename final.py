#firebase
import firebase_admin
from firebase_admin import db, credentials
#time
from datetime import datetime
import time
#adc
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

#GLOBALS
numberOfSamples = 10

#FIREBASE SETUP
#authenticate to the database
cred = credentials.Certificate("/home/cdrobertson/Proj/final/credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://iotproject-7f9d4-default-rtdb.firebaseio.com/"})
#create reference to root node
rootRef = db.reference("/")


#I2C SETUP
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# Create a single ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

#MAIN LOOP
try:
    while True:
        #collect samples and find average
        averageValue = 0
        averageVoltage = 0
        for i in range(0, numberOfSamples): #collect samples
            averageValue += chan.value
            averageVoltage += chan.voltage
            time.sleep(0.05)
        averageValue /= numberOfSamples
        averageVoltage /= numberOfSamples

        #get current time
        currentDateAndTime = str(datetime.now())
        year = currentDateAndTime[:4]
        month = currentDateAndTime[5:7]
        day = currentDateAndTime[8:10]
        currentTime = currentDateAndTime[11:19] #don't call this "time" it will conflict with time library
        currentRef = db.reference(f"/{year}/{month}/{day}")

        #update database
        keyString = f"Value and Voltage at {currentTime}"
        valueTuple = (averageValue, averageVoltage)
        print(keyString)
        print(valueTuple)
        currentRef.update({keyString: valueTuple}) #send keyString
        time.sleep(25)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
#ref.update({"testKey": [0, 1, 2, 6, 100]})
