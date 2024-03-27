from fastapi import APIRouter
from backend.models.request import TextRequest
from backend.models.client import OllamaClient
from backend.settings import config
import os

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

modelClient = OllamaClient(config.ollama_url, config.current_model)
dirname = os.path.dirname(__file__)


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.post("/send_text_request")
def handle_text_request(parameters: TextRequest):
    return {
        "course": parameters.course,
        "subject": parameters.subject,
        "text": parameters.text,
        "is_ok": "ok"
    }


@router.get("/ask_model_by_text_request")
def ask_model_by_text(course : str, subject : str, text : str):
    modelClient.readContextFromFile(os.path.join(dirname, '../../parser/new_data.json'), course, subject)
    answer = modelClient.sendPrompt(text)
    return answer

