from __future__ import absolute_import, unicode_literals
from celery import Celery
from decouple import config
import django
import os

# Command to run from a terminal to start workers :
# celery -A administrator worker -l info

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webinterface.settings')

app = Celery('administrator', backend='redis://localhost', broker='amqp://guest:guest@localhost:5672//')

#app.conf.broker_url = 'redis://localhost:6379/0'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))