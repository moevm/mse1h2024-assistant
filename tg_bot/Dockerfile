FROM python:3.9
#RUN sudo chmod -R 777 /var/lib sudo apt-get install python3.9-venv

WORKDIR /tg_bot
COPY . /tg_bot
RUN chmod +x /tg_bot/bot.py
RUN pip install --no-cache-dir --upgrade -r /tg_bot/requirements.txt
CMD python3 /tg_bot/bot.py
