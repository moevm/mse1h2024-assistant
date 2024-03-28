from pydantic import BaseModel


class TextRequest(BaseModel):
    course: str
    subject: str
    text: str