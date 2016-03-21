import spidev
from time import sleep
import math

#CONFIGURATION
Rref = 400                  # Rref = 400 for PT100, Rref = 4000 for PT1000
HowToRound = 2
spi = spidev.SpiDev()
#END OF CONFIGURATION


def configure_max31865():
    global spi
    spi.open(0, 0)
    spi.mode = 3
    lst = [0x80, 0xc2]  # should be [0x80,0xc2] if 2 or 4 wire probe, [0x80,0xD2] for 3 wire probe.
    spi.writebytes(lst)


def calendar_van_dusen(R):
    a = 3.9083E-03
    b = -5.7750E-07
    R0 = Rref/4

    return (-R0*a+math.sqrt(R0*R0*a*a-4*R0*b*(R0-R)))/(2*R0*b);



def getPT100():
    reg = spi.readbytes(9)
    del reg[0]                      # delete 0th dummy data
    RTDdata = reg[1] << 8 | reg[2]
    ADCcode = RTDdata >> 1
    R = ADCcode * Rref / 32768
    return round(calendar_van_dusen(R), HowToRound)
