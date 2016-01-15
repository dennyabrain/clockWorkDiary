from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def pollTurk():
	print('this job runs every 5 seconds')

sched.start()