import spidev
import math
import os
import glob
import time




def configure_ds1820():
    global device_file

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'


def configure_max31865():
    global spi
    spi.open(0, 0)
    spi.mode = 3
    lst = [0x80, 0xc2]  # should be [0x80,0xc2] if 2 or 4 wire probe, [0x80,0xD2] for 3 wire probe.
    spi.writebytes(lst)


def calendar_van_dusen(R):
    a = 3.9083E-03
    b = -.7750E-07
    R0 = Rref/4

    return (-R0*a+math.sqrt(R0*R0*a*a-4*R0*b*(R0-R)))/(2*R0*b);


def getPT100():
    reg = spi.readbytes(9)
    del reg[0]                      # delete 0th dummy data
    RTDdata = reg[1] << 8 | reg[2]
    ADCcode = RTDdata >> 1
    R = ADCcode * Rref / 32768
    return round(calendar_van_dusen(R), HowToRound)


def configure_max31865():
    global spi
    spi.open(0, 0)
    spi.mode = 3
    lst = [0x80, 0xc2]  # should be [0x80,0xc2] if 2 or 4 wire probe, [0x80,0xD2] for 3 wire probe.
    spi.writebytes(lst)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

