# Siglent-SDG-800-Generator-Controller
## Brief
Basic GUI to control a Siglent SDG 800 signal generator though USB

## Prerequisites
1. National Instruments VISA drivers: https://www.ni.com/en-ie/support/downloads/drivers/download.ni-visa.html#329456

2. Python 3 interpreter
3. Python packages (pip install ..) 
   - pyvisa
   - pyvisa-pi
   - tkinter

## Step by step to use
Download/clone the repo
Open your system terminal and navigate to the repo folder. There, execute the following commands:
  - python -m venv venv
  - venv/Scripts/activate
  - pip install pyvisa
  - pip install pyvisa-pi
  - pip install tkinter
  
and finally run the python script:
  - python GeneratorGui.py
