FROM python:3.9
#RUN sudo chmod -R 777 /var/lib sudo apt-get install python3.9-venv

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./backend /backend/backend
COPY ./parser /backend/parser

COPY ./pytest.ini /backend/pytest.ini
COPY ./tests /backend/tests