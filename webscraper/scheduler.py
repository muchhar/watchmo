from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .jobs import schedule_api,get_gameid


def start():
    scheduler = BackgroundScheduler()
    
    existing_jobs = scheduler.get_jobs()

    # Define the job you want to add
    job_to_add = scheduler.add_job(schedule_api, 'interval', seconds=90)
    job_to_add2 = scheduler.add_job(get_gameid,'interval',seconds=691200) #8days
    # # Check if the job is not in the list of existing jobs
    try:
        if job_to_add not in existing_jobs:
            print("Adding the job to the scheduler.")
            scheduler.start()
        else:
            print("The job is already in the scheduler.")
    except:
        pass

    try:
        if job_to_add2 not in existing_jobs:
            print("Adding the job to the scheduler.")
            scheduler.start()
        else:
            print("The job is already in the scheduler.")
    except:
        pass
