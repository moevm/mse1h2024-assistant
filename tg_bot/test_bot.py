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
    assert "Ваш запрос слишком длинный! Максимальная поддерживаемая длина" in response.text


def test_send_long_audio_to_backend(backend_url):
    course = '1'
    subject = 'Информатика'
    logger = build_logger('test_logger')

    # Генерация тестового аудиофайла длиной более 20 секунд
    sample_rate = 44100  # 44.1 kHz
    duration = 21  # 21 seconds
    num_samples = sample_rate * duration
    audio_data = (b'\x00\x00' * num_samples)

    audio_blob = io.BytesIO()
    with wave.open(audio_blob, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

    audio_blob.seek(0)

    response = send_voice_to_backend(backend_url, course, subject, audio_blob, logger)

    assert response is not None
    assert "Ваше аудиосообщение слишком длинное! Пожалуйста, запишите его покороче" in response.text
