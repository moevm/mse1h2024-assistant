import requests
import json


def send_text_to_backend(backend_url, course, subject, question, logger):
    payload = {'course': course, 'subject': subject, 'text': question}
    encoded_payload = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    logger.info("Отправка данных на бэкэнд: %s", encoded_payload.decode('utf-8'))
    try:
        response = requests.post(backend_url, encoded_payload)
        response_data = response.json()
        response_text = response_data.get("text")
        if response_text:
            logger.info("Получен ответ от сервера: %s", response_text)
            return response_text
        else:
            logger.warning("В ответе отсутствует поле 'text': %s", response_data)
            return None
    except Exception as e:
        logger.error("Произошла ошибка при отправке данных на бэкэнд: %s", str(e))


def handle_text_message(message, user_data, bot, backend_url, logger):
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
        bot.reply_to(message, "Твое сообщение обрабатывается.")
        response_text = send_text_to_backend(backend_url, course, subject, question, logger)
        if response_text:
            bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, "При получении ответа произошла ошибка.")
        bot.send_message(message.chat.id, "Введите ваш курс.")
        user_data[message.from_user.id]['state'] = 'course'


def handle_voice_message(message, user_data, bot, backend_url, logger):
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
        response_text = send_text_to_backend(backend_url, course, subject, voice_string, logger)

        if response_text:
            bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, "При получении ответа произошла ошибка.")

        bot.send_message(message.chat.id, "Введите ваш курс.")
        user_data[message.from_user.id]['state'] = 'course'
