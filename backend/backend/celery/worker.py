import time
import os
from celery import Celery
from backend.settings import config

broker = config.celery_broker_url
backend = config.celery_backend_url

# celery = Celery(__name__, backend=backend, broker=backend)

# used for backend on host machine container
celery = Celery(__name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0")

@celery.task(name="example_task")
def example_task(text = ""):
    time.sleep(30)
    return "[HANDELED] " + text
    