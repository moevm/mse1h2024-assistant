from fastapi.testclient import TestClient
import unittest
from typing import Dict
from backend.main import app


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

    
