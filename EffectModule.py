import threading
import time
import RPi.GPIO as GPIO


class EffectModule (threading.Thread):

    def __init__(self, element, effect):
        threading.Thread.__init__(self)
        self.element = element
        self.effect = effect

    def run(self):
        self.set_effect()

    def set_effect(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(self.element, GPIO.LOW)
        while True:
            try:
                GPIO.output(self.element, GPIO.HIGH)
                time.sleep(self.effect / 100)
                GPIO.output(self.element, GPIO.LOW)
                time.sleep((100 - self.effect) / 100)
            except:
                return
