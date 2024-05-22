import requests
import json
import time


def send_text_to_backend(backend_url, course, subject, question, logger):
    payload = {'course': course, 'subject': subject, 'text': question}
    encoded_payload = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    logger.info("Отправка данных на бэкэнд: %s", encoded_payload.decode('utf-8'))

    response = requests.post(f"{backend_url}/api/ask_model_by_text_request", encoded_payload)
    task_id = response.json().get('text')

    if task_id:
        result = get_task_result(task_id, backend_url, logger)
        return result
    else:
        logger.error("В ответе отсутствует поле 'text'")


def send_voice_to_backend(backend_url, course, subject, audio_blob, logger):
    logger.info("Голосовое отправлено")
    try:
        response = requests.post(
            f"{backend_url}/api/send_voice_request",
            data={"course": course, "subject": subject},
            files={"audio": audio_blob}
        )
        response_data = response.json()
        response_text = response_data.get("text")
        if response_text:
            logger.info(f"Получен ответ от сервера: {response_text}")
            return response_text
        else:
            logger.warning(f"В ответе отсутствует поле 'text': {response_data}")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при отправке голосовых данных на бэкэнд: {str(e)}")
        return None


def get_task_result(task_id, backend_url, logger):
    while True:
        response = requests.get(f"{backend_url}/api/tasks/{task_id}")
        data = response.json()

        if data.get('task_status') == 'SUCCESS':
            return data.get('task_result')

        logger.info(f"res: {data}")
        time.sleep(5)


def handle_text_message(message, user_data, bot, backend_url, logger):
    user_id = message.from_user.id
    user_state = user_data.get(user_id, {}).get('state')

    if user_data.get(user_id, {}).get('processing'):
        bot.send_message(message.chat.id, "Ваш запрос ещё обрабатывается. Пожалуйста, подождите.")
        return

    if user_state == 'course':
        if not message.text.isdigit():
            bot.send_message(message.chat.id, "Курс должен быть числом. Попробуйте еще раз.")
            return
        user_data[user_id]['course'] = message.text
        bot.send_message(message.chat.id, "Пожалуйста, введите предмет.")
        user_data[user_id]['state'] = 'subject'
    elif user_state == 'subject':
        user_data[user_id]['subject'] = message.text
        bot.send_message(message.chat.id, "Задайте ваш вопрос.")
        user_data[user_id]['state'] = 'question'
    elif user_state == 'question':
        course = user_data[user_id]['course']
        subject = user_data[user_id]['subject']
        question = message.text
        bot.reply_to(message, "Твое сообщение обрабатывается.")
        user_data[user_id]['processing'] = True
        response_text = send_text_to_backend(backend_url, course, subject, question, logger)
        if response_text:
            bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, "При получении ответа произошла ошибка.")
        bot.send_message(message.chat.id, "Введите ваш курс.")
        user_data[user_id]['state'] = 'course'
        user_data[user_id]['processing'] = False


def handle_voice_message(message, user_data, bot, backend_url, logger):
    user_id = message.from_user.id

    if user_data.get(user_id, {}).get('processing'):
        bot.send_message(message.chat.id, "Ваш запрос ещё обрабатывается. Пожалуйста, подождите.")
        return

    if 'course' not in user_data[user_id] or 'subject' not in user_data[user_id]:
        bot.reply_to(message, "Для начала введите курс и предмет, используя команду \start.")
    else:
        if message.voice.duration > 12:
            bot.reply_to(message,
                         "Ваше аудиосообщение слишком долгое! Пожалуйста, запишите вопрос покороче. Максимальная "
                         "длительность: 12 сек.")
            return
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        voice_file = bot.download_file(file_info.file_path)
        voice_string = voice_file.decode('latin-1')
        bot.reply_to(message, "Твое голосовое сообщение обрабатывается.")
        user_data[user_id]['processing'] = True

        course = user_data[user_id]['course']
        subject = user_data[user_id]['subject']
        response_text = send_voice_to_backend(backend_url, course, subject, voice_string, logger)

        if response_text:
            bot.send_message(message.chat.id, response_text)
        else:
            bot.send_message(message.chat.id, "При получении ответа произошла ошибка.")

        bot.send_message(message.chat.id, "Введите ваш курс.")
        user_data[user_id]['state'] = 'course'
        user_data[user_id]['processing'] = False
