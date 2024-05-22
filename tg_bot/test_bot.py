import pytest
import configparser
import wave
import io
from modules.handlers import send_text_to_backend, send_voice_to_backend
from modules.logger import build_logger


@pytest.fixture
def backend_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get('Backend', 'url')


def test_send_text_to_backend(backend_url):
    course = '1'
    subject = 'Информатика'
    question = 'Рейтинг'
    logger = build_logger('test_logger')

    response = send_text_to_backend(backend_url, course, subject, question, logger)

    assert response is not None


def test_send_voice_to_backend(backend_url):
    course = '1'
    subject = 'Информатика'
    audio_blob = b'audio_data'
    logger = build_logger('test_logger')

    response = send_voice_to_backend(backend_url, course, subject, audio_blob, logger)

    assert response is not None


def test_send_long_text_to_backend(backend_url):
    course = '1'
    subject = 'Информатика'
    long_question = 'a' * 200
    logger = build_logger('test_logger')

    response = send_text_to_backend(backend_url, course, subject, long_question, logger)

    assert response is not None
    assert "Ваш запрос слишком длинный! Максимальная поддерживаемая длина - 100 знаков." in response
