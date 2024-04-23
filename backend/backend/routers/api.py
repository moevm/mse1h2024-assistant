from fastapi import APIRouter, Form, File, UploadFile
from fastapi.requests import Request
from typing import Dict
from backend.models.request import TextRequest, MultipleTasksRequest
from backend.models.client import OllamaClient
from backend.settings import config
from backend.celery.worker import example_task, text_request_handling
from backend.celery.tasks import getTaskResult, getTasksStatus, deleteTasks
from backend.translator.translator import translate
import requests
import os
import json

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

modelClient = OllamaClient(config.ollama_url, config.current_model)
dirname = os.path.dirname(__file__)


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get("/get_courses")
def send_courses():
    with open("./parser/new_data.json", encoding="utf-8") as json_file:
        data = json.load(json_file)
    res = {}
    for i in list(data.keys()):
        if i != "date":
            course = i
            if course == "info":
                course = "Информация"
            res[course] = []
            for item in data[i]:
                res[course].append(item["name"])
    return res


@router.post("/ask_model_by_text_request")
def ask_model_by_text(request: TextRequest):
    task = text_request_handling.apply_async([],{"request": request.text, "course": request.course, "subject": request.subject})
    return {'text': task.id}

@router.post("/send_voice_request")
async def handle_voice_request(request: Request):
    url = "http://whisper:9000/asr"
    form = await request.form()
    form_dict: Dict = form.__dict__['_dict']

    payload = {
        "input": {
            "encode": True,
            "task": "transcribe",
            "language": "ru",
            "vad_filter": True,
            "word_timestamps": False,
            "output": "txt"
        },
    }
    headers = {
        "content-type": 'multipart/form-data'
    }
    print(form_dict)

    transcription = requests.post(url, json=payload, headers=headers, data=form_dict['audio'])

    print("Transcript: ", transcription.text)
    task = text_request_handling.apply_async([],{"request": transcription.text, "course": form_dict['course'], "subject": form_dict['subject']})
    return {'text': task.id}



@router.post("/celery_example/{text}")
def celery_example(text):
    task = example_task.apply_async([],{"text": text})
    return {'task_id': task.id}

@router.get("/tasks/{task_id}")
def get_status(task_id):
    return getTaskResult(task_id)

@router.post("/tasks/status")
def get_status(request: MultipleTasksRequest):
    return getTasksStatus(request.task_id_list)

@router.delete("/tasks/delete")
def get_status(request: MultipleTasksRequest):
    deleteTasks(request.task_id_list)
    return {"ok": True}