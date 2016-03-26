import os
from Config import *
from EffectModule import *
from ARCController import Controller
import time

if __name__ == '__main__':
    controller = Controller()
    thread = EffectModule(Element1, 50)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        thread.start()
        while True:
            controller.run()
            time.sleep(3)
    # except (KeyboardInterrupt, SystemExit, Exception):
    except:
        print("Done!")

    finally:
        GPIO.setmode(GPIO.BOARD)
        for i in PinList:
            GPIO.output(i, GPIO.LOW)

        GPIO.cleanup()



