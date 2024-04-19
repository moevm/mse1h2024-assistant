from fastapi import APIRouter, Form, File, UploadFile
from fastapi.requests import Request
from typing import Dict
from backend.models.request import TextRequest
from backend.models.client import OllamaClient
from backend.settings import config
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
    modelClient.readContextFromFile(os.path.join(dirname, '../../parser/new_data.json'), request.course,
                                    request.subject)
    answer = modelClient.sendPrompt(request.text)
    return {'text': answer}


@router.post("/send_voice_request")
async def handle_voice_request(request: Request):
    url = "http://172.19.0.4:9000/asr"
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
    modelClient.readContextFromFile(os.path.join(dirname, '../../parser/new_data.json'), course, subject)
    answer = modelClient.sendPrompt(transcription.text)
    return {'text': answer}
