from fastapi.testclient import TestClient
from pydantic import BaseModel
import unittest
from typing import Dict
from backend.main import app
from backend.celery.worker import text_request_handling, example_task
from unittest.mock import Mock, patch

class TestRouters(unittest.TestCase):
    """Класс тестирования роутов бэкенда."""

    def setUp(self) -> None:
        self.client = TestClient(app)

        return


    def tearDown(self) -> None:
        self.client.close()
        return
    
    def test_get_courses(self):

        response = self.client.get("/api/get_courses")
        self.assertEqual(response.status_code, 200)

        response: Dict = response.json()
        courses = ['1 курс', '2 курс', '3 курс', '4 курс', '5 курс', '6 курс']
        
        for course in courses:
            self.assertIn(course, response)

    @patch('backend.celery.worker.text_request_handling.apply_async')
    def test_ask_model_by_text(self, mock_handler) -> None:

        class TestTask(BaseModel):
            id: int 
        
        task = TestTask(id=1)

        mock_handler.return_value = task
        response = self.client.post(
            "/api/ask_model_by_text_request",
             headers={
                 "Content-Type": "application/json",
             },
             json={
                "course": "1 курс",
                "subject": "программирование",
                "text": "как дела?",
             },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'text': task.id})
    
