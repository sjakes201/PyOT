import schedule
import time
import threading
from datetime import datetime



#DEFINE JOBS HERE

options_to_update = [] #Later change to access the options inside position manager or something
def JOB_update_options():
        for i in range(len(options_to_update)):
            t = threading.Thread(target=options_to_update[i].update_value)
            t.start()






#RUNNING JOBS, CALL start_jobs to start all jobs
def start_jobs():
    def __job_cycler():
        #INSERT JOBS INTO HERE
        schedule.every(5).seconds.do(JOB_update_options)





        while 1:
            schedule.run_pending()
            time.sleep(1)

    jobs = threading.Thread(target=__job_cycler) #thread so that the program can continue running after start_jobs() is called
    jobs.start()
