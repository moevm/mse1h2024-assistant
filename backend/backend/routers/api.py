from fastapi import APIRouter, Form, File, UploadFile
from fastapi.requests import Request
from typing import Dict
from backend.models.request import TextRequest, MultipleTasksRequest
from backend.models.client import OllamaClient
from backend.settings import config
from backend.celery.worker import audio_request_handling, text_request_handling, completed_task
from backend.celery.tasks import getTaskResult, getTasksStatus, deleteTasks
from backend.translator.translator import translate
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
    # check that len text request less than limit
    if(len(request.text) > config.text_request_limit):
        error_text = "Ваш запрос слишком длинный! Максимальная поддерживаемая длина - 100 знаков.(У вас - {}) Пожалуйста, задайте вопрос по другому.".format(len(request.text))
        task = completed_task.apply_async([],{"text": error_text})
        return {'text': task.id}
    else:
        task = text_request_handling.apply_async([],{"request": request.text, "course": request.course, "subject": request.subject})
        return {'text': task.id}

@router.post("/send_voice_request")
async def handle_voice_request(request: Request):
    form = await request.form()
    form_dict: Dict = form.__dict__['_dict']
    content: UploadFile = form_dict['audio']
    audio_content = await content.read()
    task = audio_request_handling.apply_async([],{"audio_bytes": audio_content, "course": form_dict['course'], "subject": form_dict['subject']})
    return {'text': task.id}

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