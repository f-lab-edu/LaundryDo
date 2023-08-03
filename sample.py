from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def display(msg) :
    print(msg)
    # scheduler.shutdown(wait = False)

scheduler = BlockingScheduler()

msg = 'hello'
scheduler.add_job(display, 'interval', seconds = 3, args = [input('enter something..')])
scheduler.add_job(display, 'interval', seconds = 5, args = ['job2'])


scheduler.start()