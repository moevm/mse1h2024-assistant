import sys
import telebot
import configparser
from modules.handlers import handle_text_message, handle_voice_message
from modules.logger import build_logger


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    bot_token = config.get('Telegram', 'bot_token')
    backend_url = config.get('Backend', 'url')

    return bot_token, backend_url


bot_token, backend_url = read_config()
bot = telebot.TeleBot(bot_token)
logger = build_logger('my_logger')
user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать!\nБот не несет ответственности за представленную информацию\nВведите свой курс.")
    user_data[message.from_user.id] = {'state': 'course'}


@bot.message_handler(content_types=['voice'])
def process_voice_message(message):
    handle_voice_message(message, user_data, bot, backend_url, logger)


@bot.message_handler(func=lambda message: True)
def process_text_message(message):
    handle_text_message(message, user_data, bot, backend_url, logger)


if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        logger.error("An error occurred while running the bot: %s", str(e))
        sys.exit(1)
