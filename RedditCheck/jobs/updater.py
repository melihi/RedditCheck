from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api
 
def start():
    # set scheduler 
    # scheduler starts crawling  every 1 minute
    # if crawling not finished not starttin new instance
   
         scheduler = BackgroundScheduler(daemon=True)
         scheduler.add_job(schedule_api,'interval', minutes=1,max_instances=1)
         


         scheduler.start()
    