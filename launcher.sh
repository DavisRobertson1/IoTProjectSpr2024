#!/bin/bash
# launcher.sh
# navigate home, then to this directory, activate the virtual environment,
# execute finalNoLoop.py, then navigate back home

#wait for the network to be ready
sleep 30


cd /
cd home/cdrobertson/Proj/final

# Activate the virtual environment
source /home/cdrobertson/ads1115_env/bin/activate

# Run the Python script
python3 finalNoLoop.py

# Deactivate the virtual environment
deactivate

cd /

