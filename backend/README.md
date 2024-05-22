# backend

# Тестирование
1. Проект должен быть запущен по основной инструкции

Находясь в mse1h2024-assistant/backend:

2. Сборка тестового контейнера: \
```docker build -f DockerfileTest . -t backend_test```
3. Запуск тестового контейнера и тестов: \
```docker run --name backend_test --network mse1h2024-assistant_main -d backend_test```
4. Запуск юнит-тестов: \
```docker exec -it backend_test bash -c "cd ./tests && python3 -m unittest test_routers.py"```
5. Запуск интеграционных тестов: \
```docker exec -it backend_test bash -c "cd ./tests && python -m pytest -m integration"```
