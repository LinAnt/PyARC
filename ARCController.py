import glob
import math
import os
import time
import spidev
import RPi.GPIO as GPIO

from Config import *


class Controller:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.spi = spidev.SpiDev()
        self.state = 0
        self.StableTemperature = StableTemperature
        self.StateTime = StateTime
        self.device_file = device_file
        self.states = {0: self.heat_up,
                       1: self.stabilize,
                       2: self.circulation,
                       3: self.reheat,
                       }
        self.configure_ds1820()
        self.configure_max31865()
        # Setup GPIO and ensure the pins start as LOW
        for i in PinList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

    def run(self):
        self.state = self.states[self.state]()

    def print_state(self):
        print('State: ', self.state, 'StateTime', self.StateTime, 'StableTemp:' , self.StableTemperature,
              'Current PT100', self.getPT100())

    def configure_max31865(self):
        self.spi.open(0, 0)
        self.spi.mode = 3
        lst = [0x80, 0xc2]  # should be [0x80,0xc2] if 2 or 4 wire probe, [0x80,0xD2] for 3 wire probe.
        self.spi.writebytes(lst)

    def heat_up(self):
        GPIO.output(Element1, GPIO.HIGH)
        GPIO.output(Element2, GPIO.HIGH)
        if self.read_temp() > HeatUpTemperature:
            return 1
        else:
            return 0

    def stabilize(self):
        GPIO.output(Element1, GPIO.HIGH)
        GPIO.output(Element2, GPIO.LOW)
        if self.StateTime < 0:
            self.StateTime = time.time()
            return 1

        elif time.time() - self.StateTime < StabilizationTime:
            return 1

        else:
            self.StableTemperature = self.getPT100()
            return 2

    def circulation(self):
        if self.read_temp() >= MaxTemperature:
            shutdown(0)

        GPIO.output(Solenoid, GPIO.HIGH)
        if abs(StableTemperature - self.getPT100()) < 0.1:
            GPIO.output(Solenoid, GPIO.LOW)
            return 2
        else:
            return 3

    def reheat(self):
        if self.read_temp() >= MaxTemperature:
            shutdown(0)
        GPIO.output(Solenoid, GPIO.LOW)
        if StableTemperature == self.getPT100():
            return 2
        else:
            return 3

    def configure_ds1820(self):

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def calendar_van_dusen(self, R):
        a = 3.9083E-03
        b = -.7750E-07
        R0 = Rref / 4

        return (-R0 * a + math.sqrt(R0 * R0 * a * a - 4 * R0 * b * (R0 - R))) / (2 * R0 * b);

    def getPT100(self):
        reg = self.spi.readbytes(9)
        del reg[0]  # delete 0th dummy data
        RTDdata = reg[1] << 8 | reg[2]
        ADCcode = RTDdata >> 1
        R = ADCcode * Rref / 32768
        return round(self.calendar_van_dusen(R), HowToRound)

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c


def shutdown(code):
    for i in PinList:
        GPIO.output(i, GPIO.LOW)

    GPIO.cleanup()
    SystemExit(code)
