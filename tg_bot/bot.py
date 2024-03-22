import io
import json

import telebot
import requests
import logging

bot_token = '7189687900:AAE1uagUpFOp5PKE6r-MRWaWNYZiAoEob-8'
bot = telebot.TeleBot(bot_token)

user_data = {}

backend_url = 'http://localhost:5000/api/send_text_request'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!\nБот не несет ответственности за представленную информацию\nВведите свой курс.")
    user_data[message.from_user.id] = {'state': 'course'}


def handle_text_message(message):
    user_state = user_data.get(message.from_user.id, {}).get('state')

    if user_state == 'course':
        user_data[message.from_user.id]['course'] = message.text
        bot.send_message(message.chat.id, "Пожалуйста, введите предмет.")
        user_data[message.from_user.id]['state'] = 'subject'
    elif user_state == 'subject':
        user_data[message.from_user.id]['subject'] = message.text
        bot.send_message(message.chat.id, "Задайте ваш вопрос.")
        user_data[message.from_user.id]['state'] = 'question'
    elif user_state == 'question':
        course = user_data[message.from_user.id]['course']
        subject = user_data[message.from_user.id]['subject']
        question = message.text
        send_text_to_backend(course, subject, question)
        bot.reply_to(message, "Твое сообщение обрабатывается.")
        user_data[message.from_user.id] = {'state': 'course'}


def handle_voice_message(message):
    if 'course' not in user_data[message.from_user.id] or 'subject' not in user_data[message.from_user.id]:
        bot.reply_to(message, "Для начала введите курс и предмет, используя команду \start")
    else:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        voice_file = bot.download_file(file_info.file_path)
        voice_blob = io.BytesIO(voice_file)
        voice_blob.seek(0)
        voice_data = voice_blob.read()
        voice_string = voice_data.decode('latin-1')
        bot.reply_to(message, "Твое голосовое сообщение обрабатывается.")

        course = user_data[message.from_user.id]['course']
        subject = user_data[message.from_user.id]['subject']
        send_text_to_backend(course, subject, voice_string)

        user_data[message.from_user.id] = {'state': 'course'}


def send_text_to_backend(course, subject, question):
    payload = {'course': int(course), 'subject': subject, 'text': question}
    json_payload = json.dumps(payload)
    try:
        response = requests.post(backend_url, data=json_payload)
        if response.status_code == 200:
            logger.info("Text data sent to backend successfully.")
        else:
            logger.error("Error sending text data to backend: %s", response.status_code)
    except Exception as e:
        logger.error("An error occurred while sending text data to backend: %s", str(e))


@bot.message_handler(content_types=['voice'])
def process_voice_message(message):
    handle_voice_message(message)


@bot.message_handler(func=lambda message: True)
def process_text_message(message):
    handle_text_message(message)


if __name__ == '__main__':
    bot.polling()
