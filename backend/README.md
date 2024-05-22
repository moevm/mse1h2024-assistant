# backend

# Тестирование
1. Проект должен быть запущен по основной инструкции

Находясь в mse1h2024-assistant/backend:

2. Сборка тестового контейнера: \
```docker build -t backend_test -f DockerfileTest .```
3. Запуск тестового контейнера и тестов: \
```docker run --network mse1h2024-assistant_main -d backend_test```
4. Запуск юнит-тестов: \
```docker exec -it <id контейнера> bash -c "cd ./tests && python3 -m unittest test_routers.py```
5. Запуск интеграционных тестов: \
```docker exec -it  <id контейнера>  pytest ./tests/test_whisper.py```
