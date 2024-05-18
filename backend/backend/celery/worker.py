import time
import os
import requests
from celery import Celery
from backend.settings import config
from backend.models.client import OllamaClient
from backend.translator.translator import translate

broker = config.celery_broker_url
backend = config.celery_backend_url

celery = Celery(__name__, backend=backend, broker=backend)

# used for backend on host machine
# celery = Celery(__name__, backend="redis://localhost:6379/0", broker="redis://localhost:6379/0")

modelClient = OllamaClient(config.ollama_url, config.current_model)
dirname = os.path.dirname(__file__)

@celery.task(name="example_task")
def example_task(text = ""):
    time.sleep(30)
    return "[HANDELED] " + text

@celery.task(name="completed_task")
def completed_task(text = ""):
    return text

@celery.task(name="text_request_handling")
def text_request_handling(request = "", course = "", subject = ""):
    modelClient.readContextFromFile(os.path.join(dirname, '../../parser/new_data.json'), course, subject)
    answer = modelClient.sendPrompt(request)
    answer = translate(answer)
    return answer