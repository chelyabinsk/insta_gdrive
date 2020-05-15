from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
import insta_test

@sched.scheduled_job('cron', hour=6)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
