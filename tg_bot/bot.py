import json
import sys

import telebot
import requests
import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    bot_token = config.get('Telegram', 'bot_token')
    backend_url = config.get('Backend', 'url')

    return bot_token, backend_url


def send_text_to_backend(backend_url, course, subject, question):
    payload = {'course': course, 'subject': subject, 'text': question}
    print(json.dumps(payload))
    try:
        response = requests.post(backend_url, json.dumps(payload))
        response_data = response.json()
        print(response_data)
        response_text = response_data.get("text")
        if response_text:
            print("RESPONSE:", response_text)
            return response_text
        else:
            print("No 'text' field in response:", response_data)
            return None
    except Exception as e:
        print("An error occurred while sending text data to backend:", str(e))


def handle_text_message(message, user_data, bot, backend_url):
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
        send_text_to_backend(backend_url, course, subject, question)
        bot.reply_to(message, "Твое сообщение обрабатывается.")
        user_data[message.from_user.id] = {'state': 'course'}


def handle_voice_message(message, user_data, bot, backend_url):
    if 'course' not in user_data[message.from_user.id] or 'subject' not in user_data[message.from_user.id]:
        bot.reply_to(message, "Для начала введите курс и предмет, используя команду \start")
    else:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        voice_file = bot.download_file(file_info.file_path)
        voice_string = voice_file.decode('latin-1')
        bot.reply_to(message, "Твое голосовое сообщение обрабатывается.")

        course = user_data[message.from_user.id]['course']
        subject = user_data[message.from_user.id]['subject']
        send_text_to_backend(backend_url, course, subject, voice_string)

        user_data[message.from_user.id] = {'state': 'course'}


def main():
    bot_token, backend_url = read_config()
    bot = telebot.TeleBot(bot_token)

    user_data = {}

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id,
                         "Добро пожаловать!\nБот не несет ответственности за представленную информацию\nВведите свой курс.")
        user_data[message.from_user.id] = {'state': 'course'}

    @bot.message_handler(content_types=['voice'])
    def process_voice_message(message):
        handle_voice_message(message, user_data, bot, backend_url)

    @bot.message_handler(func=lambda message: True)
    def process_text_message(message):
        handle_text_message(message, user_data, bot, backend_url)

    try:
        bot.polling()
    except Exception as e:
        print("An error occurred while running the bot:", str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
