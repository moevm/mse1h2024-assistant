import pytest
import requests
import configparser

from modules.handlers import send_text_to_backend, send_voice_to_backend, get_task_result
from modules.logger import build_logger


@pytest.fixture
def backend_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('Backend', 'url')


# def test_send_text_to_backend(backend_url):
#     course = '1'
#     subject = 'Информатика'
#     question = 'Рейтинг'
#     logger = build_logger('test_logger')
#
#     response = send_text_to_backend(backend_url, course, subject, question, logger)
#
#     assert response is not None
#
#
# def test_send_voice_to_backend(backend_url):
#     course = '1'
#     subject = 'Информатика'
#     audio_blob = b'audio_data'
#     logger = build_logger('test_logger')
#
#     response = send_voice_to_backend(backend_url, course, subject, audio_blob, logger)
#
#     assert response is not None


def test_send_text_to_backend_with_long_message(backend_url):
    course = '1'
    subject = 'Информатика'
    question = 'A' * 150
    logger = build_logger('test_logger')

    response = send_text_to_backend(backend_url, course, subject, question, logger)

    assert response == "Длина сообщения не должна превышать 100 символов."
