from fastapi import APIRouter, Form, File, UploadFile
import requests
from backend.decoder.whisper import model, trunscribe
from backend.models.request import TextRequest

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

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

@router.post("/send_voice_request")
def handle_voice_request(course: int = Form(...), subject: str = Form(...), audio: UploadFile = File(...)):
    
    decoded = trunscribe(audio.file)
    
    return {
        "course": course,
        "subject": subject,
        "audio": audio,
        "decoded": decoded,
        "is_ok": "ok"
    }