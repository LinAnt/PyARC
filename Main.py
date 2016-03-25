import os

from apscheduler.schedulers.blocking import BlockingScheduler

from ARCController import Controller, shutdown

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    controller = Controller()
    scheduler.add_job(controller.run, 'interval', seconds=3)
    scheduler.add_job(controller.print_state, 'interval', seconds = 5)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Something unexpected happened...")
        shutdown(1)
