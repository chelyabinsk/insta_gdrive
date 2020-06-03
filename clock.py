from apscheduler.schedulers.blocking import BlockingScheduler
import ExtendTime

sched = BlockingScheduler()
import insta_test

insta_test.main()


@sched.scheduled_job('cron', hour=6)
def scheduled_job():
    insta_test.main()

sched.start()
