from pydantic import BaseModel
from typing import List


class TextRequest(BaseModel):
    course: str
    subject: str
    text: str
    
class MultipleTasksRequest(BaseModel):
    task_id_list: List[str]