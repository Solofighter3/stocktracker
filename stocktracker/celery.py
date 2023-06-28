from __future__ import absolute_import,unicode_literals
import os
import asyncio
import json
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
#Gets default config module name from enviromental variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'stocktracker.settings')
app=Celery("stocktracker")
app.conf.enable_utc=False
app.conf.update(timezone="Asia/Kathmandu")#Timezone needed for scheduling tasks
#Config is necessary to determine how celery works
#Loads config form settings which is config object and contains configuration Attribute
app.config_from_object(settings,namespace="CELERY")

#Time to schedule our api calls task in tasks.py using this configuration
app.conf.beat_schedule={
        #'every-20-seconds':{
         #   'task':'mainapp.tasks.my_task',
          #  'schedule':10,
           # 'args':(['A'],)
            #},
        #This code will call api even though our user is not present
        #For commercial purposes we can keep calling api and store 
        #Results in our django database and display when user is  present.
        #But for now we dont want to increase our api cost by  frequently calling api.
        #We want to terminate api calls whaen there are no users in our website.So,
        #we will not use this code instead we will create periodic task in consumers.py so
        #whenever our user is present our task will be initiated and will be  terminated
        #if there is no user in our websocket connection
               }

app.autodiscover_tasks()#Celery will automatically detect our tasks
@app.task(bind=True)
def debug_task(self):
    print(f"RESULT:{self.request!r}")
