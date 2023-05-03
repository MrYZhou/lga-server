from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def my_job():
    print("Job executed 1")


class Task:
    scheduler = None

    def __init__(self):
        self.scheduler = scheduler

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()


task = Task()
task.start()
