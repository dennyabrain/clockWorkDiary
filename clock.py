from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from utils import pollTurk

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def OneMinuteClock():
	print('this job runs every 5 seconds')
	result = q.enqueue(pollTurk)

sched.start()