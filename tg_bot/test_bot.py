import pytest
from unittest.mock import Mock
import configparser

from modules.handlers import handle_text_message, handle_voice_message
from modules.logger import build_logger


@pytest.fixture(scope="module")
def logger():
    return build_logger('test_logger')


@pytest.fixture(scope="module")
def mock_user_data():
    return {}


config = configparser.ConfigParser()
config.read('config.ini')
BACKEND_URL = config.get('Backend', 'url')

bot = Mock()


def test_handle_text_message(logger, mock_user_data):
    message = Mock()
    message.from_user.id = 123456
    mock_user_data[message.from_user.id] = {'state': 'course'}
    message.text = "5"
    handle_text_message(message, mock_user_data, bot, BACKEND_URL, logger)
    assert mock_user_data[message.from_user.id]['state'] == 'subject'


def test_handle_voice_message(logger, mock_user_data):
    message = Mock()
    message.from_user.id = 123456
    mock_user_data[message.from_user.id] = {'state': 'course', 'course': '5', 'subject': 'Math'}
    voice = Mock()
    voice.file_id = "voice_file_id"
    voice.duration = 15
    message.voice = voice
    handle_voice_message(message, mock_user_data, bot, BACKEND_URL, logger)
    assert mock_user_data[message.from_user.id]['state'] == 'course'
