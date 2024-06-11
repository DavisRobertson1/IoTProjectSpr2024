# Setting up the Xcode project

1. Open xcode-project/IoT_Project in Xcode

2. Change the Team and Bundle Identifier values to your own values
![](/images/image1.jpg)

3. Connect an iPhone device to your MacBook via cable

4. Enable Developer Mode on your iPhone
![](/images/image2.png)

5. Select your iPhone as the run destination
![](/images/image3.png)

6. Run

# Setting up the Raspberry Pi
To recreate the system, first connect the capacitive soil moisture sensors, ADC, and Raspberry Pi such that the ADC communicates to the Raspberry Pi via I2C and the sensors analog outputs are connected to the ADC Analog inputs.
Ensure that each of the required packages are installed on your machine or in a virtual environment which is activated in the launcher.sh file that also runs the python program. The Python file "finalNoLoop.py" includes each of the necessary packages.
Then, the crontab job must be created. Use 'sudo crontab -e' to open the crontab configuration file and at the bottom of the file, add a line similar to this (this example will run the launcher.sh every 2 minutes as long as the Raspberry Pi has power):

`*/2 * * * * /bin/bash /home/user/directory/of/launcher.sh >> /home/user/logs/yourLogFile 2>&1`

Lastly, ensure that you have a credentials.json file with the necessary Firebase Realtime Database API key in the same directory as finalNoLoop.py and the Raspberry Pi is connected to the internet.
