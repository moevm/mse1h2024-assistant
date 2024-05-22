# tg_bot

# Запуск
- Cборка контейнера:
  ```docker build -t tg_bot .```
- Запуск контейнера:
  ```docker run tg_bot```

# Тестирование
1. Проект должен быть запущен по основной инструкции
2. Сборка тестового контейнера: \
```docker build -t tg_test -f DockerfileTest .```
3. Запуск тестового контейнера и тестов \
```docker run --network mse1h2024-assistant_main tg_test```