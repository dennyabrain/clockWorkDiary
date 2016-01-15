from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from utils import printSomething

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def pollTurk():
	print('this job runs every 5 seconds')
	result = q.enqueue(printSomething)

sched.start()