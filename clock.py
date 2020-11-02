from apscheduler.schedulers.blocking import BlockingScheduler
#import ExtendTime

sched = BlockingScheduler()
from Worker import main

main()


@sched.scheduled_job('cron', hour=6)
def scheduled_job():
    main()

sched.start()
