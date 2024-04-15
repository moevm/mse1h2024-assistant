from fastapi import APIRouter
from backend.models.request import TextRequest
from backend.models.client import OllamaClient
from backend.settings import config
from backend.translator.translator import translate
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


@router.post("/ask_model_by_text_request")
def ask_model_by_text(request: TextRequest):
    modelClient.readContextFromFile(os.path.join(dirname, '../../parser/new_data.json'), request.course, request.subject)
    answer = modelClient.sendPrompt(request.text)
    return {'text': translate(answer)}

