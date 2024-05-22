from fastapi.testclient import TestClient
from fastapi import  UploadFile, Request
from pydantic import BaseModel
import unittest
from typing import Dict
from backend.main import app
from backend.celery.worker import text_request_handling
from unittest.mock import Mock, patch
import requests
from starlette.datastructures import FormData, Headers
import json

class TestTask(BaseModel):
    
    id: int 
        
task = TestTask(id=1)

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

    @patch('fastapi.Request.form')
    @patch('backend.routers.api.request_wrapper')
    @patch('backend.celery.worker.text_request_handling.apply_async')
    async def test_handle_voice_request(self, mock_form, mock_transcription, mock_hanlder):

        async def form():
            return {
            '_dict': {
                'audio': {}
                }
            }
        mock_form.return_value = await form()
        mock_transcription.return_value = 'success'
        mock_hanlder.return_value = task
        response = self.client.post(
            "/api/send_voice_request",
             headers={
                 'Content-Type': 'application/json',
             },
             data={
                "course": "1 курс",
                "subject": "программирование",
             },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'text': task.id})

if __name__ == '__main__':
    unittest.main()
        
    
