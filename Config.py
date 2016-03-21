import spidev
# This file contains all the variables for the Controller itself

# GPIO Pins for the relay board (GPIO.setmode(GPIO.BOARD))
Element1    = 11
Element2    = 13
Solenoid    = 15
ExtraRelay  = 16

# PROBE CONFIGURATION
Rref = 400                  # Rref = 400 for PT100, Rref = 4000 for PT1000
HowToRound = 2
device_file = ""

# MaxTemperature - Max temperature of the boiler
MaxTemperature = 98

# HeatUpTemperature - at which temperature should the system switch to stabilization
HeatUpTemperature = 50

# StabilizationTime - how many seconds should the Column be stable?
StabilizationTime = 18000

# Do not edit anything of the following stuff...
StateTime = 0
StableTemperature = -1
PinList = [Element1, Element2, Solenoid, ExtraRelay]  # Use when initializing the relay board
device_file = ""
spi = spidev.SpiDev()
