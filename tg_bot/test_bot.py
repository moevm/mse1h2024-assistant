# test_integration.py

import pytest
from unittest.mock import Mock
import time

# Import functions to be tested
from modules.handlers import handle_text_message, handle_voice_message
from tg_bot.modules.logger import build_logger


# Fixture for setting up logger
@pytest.fixture(scope="module")
def logger():
    return build_logger('test_logger')


# Fixture for generating mock user data
@pytest.fixture(scope="module")
def mock_user_data():
    return {}


# Mock backend URL
BACKEND_URL = "http://example.com"

# Mock bot object
bot = Mock()


# Test case for handling text message
def test_handle_text_message(logger, mock_user_data):
    message = Mock()
    message.from_user.id = 123456  # Mock user ID

    # Set user state
    mock_user_data[message.from_user.id] = {'state': 'course'}

    # Mock user input
    message.text = "5"  # Mock course

    # Call the function to be tested
    handle_text_message(message, mock_user_data, bot, BACKEND_URL, logger)

    # Check if the state has been updated
    assert mock_user_data[message.from_user.id]['state'] == 'subject'


# Test case for handling voice message
def test_handle_voice_message(logger, mock_user_data):
    message = Mock()
    message.from_user.id = 123456  # Mock user ID

    # Set user state and data
    mock_user_data[message.from_user.id] = {'state': 'course', 'course': '5', 'subject': 'Math'}

    # Mock user input
    message.voice.file_id = "voice_file_id"  # Mock file ID

    # Call the function to be tested
    handle_voice_message(message, mock_user_data, bot, BACKEND_URL, logger)

    # Check if the state has been updated
    assert mock_user_data[message.from_user.id]['state'] == 'course'
