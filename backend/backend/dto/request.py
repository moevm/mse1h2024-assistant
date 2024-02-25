from pydantic import BaseModel

class TextRequest(BaseModel):
    course: int
    subject: str
    text: str