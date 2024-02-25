from fastapi import APIRouter
from backend.dto.request import *

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
