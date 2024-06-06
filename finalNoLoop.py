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


#FUNCTIONS
#map a value from range leftMin-leftMax to corresponding value in range rightMin-rightMax
def remap(value, leftMin, leftMax, rightMin, rightMax):
    if value > leftMax:
        return rightMax
    elif value < leftMin:
        return rightMin
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    # return int(rightMin + (valueScaled * rightSpan))
    return rightMin + (valueScaled * rightSpan)

def sample(plant, numberOfSamples):
    averageValue = 0
    averageVoltage = 0
    for i in range(0, numberOfSamples): #collect samples
        averageValue += plant.channel.value
        averageVoltage += plant.channel.voltage
        time.sleep(0.05)
    plant.value = averageValue / numberOfSamples
    plant.voltage = averageVoltage / numberOfSamples
    plant.percentage = remap(
        plant.value,
        plant.sensorMinValue, plant.sensorMaxValue,     # these values comes from experiment when wet and dry
        100, 0
    )


#GLOBALS
#get current time
currentDateAndTime = str(datetime.now())
year = currentDateAndTime[:4]
month = currentDateAndTime[5:7]
day = currentDateAndTime[8:10]
currentTime = currentDateAndTime[11:19] #don't call this "time" it will conflict with time library
numberOfSamples = 10
sensorMinValues = [7750] #most moist
sensorMaxValues = [17725] #least moist
class Plant:
  def __init__(self, ID, sensorMinValue, sensorMaxValue):
    self.ID = ID
    self.sensorMinValue = sensorMinValue
    self.sensorMaxValue = sensorMaxValue
    self.channel = None
    self.percentage = None
    self.value = None
    self.voltage = None
    self.DBRef = None
plants = [Plant(i, sensorMinValues[i], sensorMaxValues[i])] for i in range(0, len(sensorMinValues))

#FIREBASE SETUP
#authenticate to the database
cred = credentials.Certificate("/home/cdrobertson/Proj/githubProject/IoTProjectSpr2024/credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://iotproject-7f9d4-default-rtdb.firebaseio.com/"})
#create reference to root node
rootRef = db.reference("/")


#I2C SETUP
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# Create a single ended input on each channel 0
possibleChannelInputs = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]
plants[i].channel = AnalogIn(ads, possibleChannelInputs[i]) for i in range(0, len(plants))
#MAIN CODE
#collect samples and find average
for plant in plants:
    sample(plant, numberOfSamples)
    plant.DBRef = db.reference(f"/{plant.ID}")
    #update database
    keyString = f"Value and Voltage on {month}-{day}-{year} at {currentTime}"
    valueList = [plant.percentage, plant.value, plant.voltage]
    print(f"Plant ID: {plant.ID}")
    print(plant.percentage)
    print(plant.value)
    print(plant.voltage)
    plant.DBRef.update({keyString: valueList}) #send keyString
