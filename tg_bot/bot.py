import io
import json
import sys
import aiohttp
import asyncio
import telebot
import requests
from modules.logger import build_logger
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    bot_token = config.get('Telegram', 'bot_token')
    backend_url = config.get('Backend', 'url')

    return bot_token, backend_url

async def main(bot):
    user_data = {}

    logger = build_logger('my_logger')

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id,
                         "Добро пожаловать!\nБот не несет ответственности за представленную информацию\nВведите свой курс.")
        user_data[message.from_user.id] = {'state': 'course'}

    def handle_text_message(message):
        user_state = user_data.get(message.from_user.id, {}).get('state')

        if user_state == 'course':
            if not message.text.isdigit():
                bot.send_message(message.chat.id, "Курс должен быть числом. Попробуйте еще раз.")
                return
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
            asyncio.run_coroutine_threadsafe(send_text_to_backend(course, subject, question), loop)
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
            asyncio.run_coroutine_threadsafe(send_text_to_backend(course, subject, voice_string), loop)

            user_data[message.from_user.id] = {'state': 'course'}

    async def send_text_to_backend(course, subject, question):
        payload = json.dumps({'course': int(course), 'subject': subject, 'text': question})
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(backend_url, json=payload) as response:
                    response_data = await response.json()
                    response_text = response_data.get("text")
                    if response_text:
                        print("RESPONSE:", response_text)
                        return response_text
                    else:
                        print("No 'text' field in response:", response_data)
                        return None
        except aiohttp.ClientError as err:
            logger(f"Error sending text data to backend: {err}")
            return None
        except Exception as e:
            logger(f"An error occurred while sending text data to backend: {e}")
            return None

    @bot.message_handler(content_types=['voice'])
    def process_voice_message(message):
        handle_voice_message(message)

    @bot.message_handler(func=lambda message: True)
    def process_text_message(message):
        handle_text_message(message)

if __name__ == '__main__':
    bot_token, backend_url = read_config()
    bot = telebot.TeleBot(bot_token)
    logger = build_logger('my_logger')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(bot))

    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        logger.error("An error occurred while running the bot: %s", str(e))
        bot.send_message("Произошла ошибка сервера")
        sys.exit(1)
