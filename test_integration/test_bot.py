import pytest
import requests
import telebot
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
BOT_TOKEN = config.get('Telegram', 'bot_token')
BACKEND_URL = config.get('Backend', 'url')
bot = telebot.TeleBot(BOT_TOKEN)


# Helper functions for sending messages to the bot
def send_text_message(bot, user_id, text):
    return bot.send_message(user_id, text)


def send_voice_message(bot, user_id, voice_file_path):
    with open(voice_file_path, 'rb') as voice_file:
        return bot.send_voice(user_id, voice_file)


def get_updates():
    return bot.get_updates()


def get_last_bot_message(user_id):
    updates = get_updates()
    messages = [update.message for update in updates if update.message and update.message.chat.id == user_id]
    if messages:
        return messages[-1].text
    return None


def get_chat_id():
    updates = get_updates()
    for update in updates:
        if update.message and update.message.text == '/start':
            return update.message.chat.id
    return None


@pytest.fixture(scope="module", autouse=True)
def setup():
    bot.remove_webhook()
    time.sleep(2)  # Ждем очистки обновлений
    updates = get_updates()  # Очищаем очередь обновлений
    bot.send_message('@your_bot_username', '/start')
    time.sleep(2)  # Ждем, чтобы бот обработал сообщение
    user_id = get_chat_id()
    assert user_id is not None
    return user_id


def test_text_message_length(setup):
    user_id = setup
    long_message = "a" * 101
    send_text_message(bot, user_id, long_message)
    time.sleep(2)  # Ждем, чтобы бот обработал сообщение
    response_text = get_last_bot_message(user_id)
    assert response_text == "Длина сообщения не должна превышать 100 символов."


# Тест для проверки длительности аудио сообщения
# def test_voice_message_duration(setup):
#     user_id = setup
#     long_voice_file = "path/to/long_voice.ogg"  # Убедитесь, что файл существует и длительность > 12 секунд
#     send_voice_message(bot, user_id, long_voice_file)
#     time.sleep(2)  # Ждем, чтобы бот обработал сообщение
#     response_text = get_last_bot_message(user_id)
#     assert response_text == "Длительность аудио не должна превышать 12 секунд."

def test_text_message_success(setup):
    user_id = setup
    valid_message = "Это валидное сообщение."
    send_text_message(bot, user_id, valid_message)
    time.sleep(2)  # Ждем, чтобы бот обработал сообщение
    response_text = get_last_bot_message(user_id)
    assert response_text == "Твое сообщение обрабатывается."

# Тест для успешной обработки голосового сообщения
# def test_voice_message_success(setup):
#     user_id = setup
#     short_voice_file = "path/to/short_voice.ogg"  # Убедитесь, что файл существует и длительность <= 12 секунд
#     send_voice_message(bot, user_id, short_voice_file)
#     time.sleep(2)  # Ждем, чтобы бот обработал сообщение
#     response_text = get_last_bot_message(user_id)
#     assert response_text == "Твое голосовое сообщение обрабатывается."
