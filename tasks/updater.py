from apscheduler.schedulers.background import BackgroundScheduler 
from .tasks import clear_user_not_verified


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_user_not_verified, 'interval', days=1)
    scheduler.start()
    