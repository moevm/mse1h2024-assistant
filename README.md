# Требования
1. Установлен docker версии > 26.1.0 \
Linux: https://docs.docker.com/engine/install/ \
Windows: https://docs.docker.com/desktop/install/windows-install/

2. Видеокарта nvidia для запуска языковой модели

3. Для использования аудиозапросов - наличие микрофона.

# Запуск проекта
1. Сборка контейнеров: 
```
docker compose build
```
2. Запуск контейнера для языковой модели: \
```
docker compose up -d ollama
```
3. Загрузка выбранной модели в контейнер:
```
docker exec -it ollama ollama pull llama3
```
4. Запуск остальных контейнеров:
```
docker compose up
```

# Проверка, что всё работает корректно
1. После запуска приложение будет доступно по адресу http://localhost:8080
2. Перейдя на стартовую страницу выберите в выпадающих списках любой курс и предмет
3. Нажмите кнопку "Начать"
4. В появившемся окне чата напишите любой интересующий вопрос и нажмите клавишу Enter или кнопку отправки
5. Ожидайте ответа от модели
6. Для проверки работы аудиосообщений нажмите на кнопку микрофона справа от строки ввода и задайте вопрос по микрофону, затем нажмите кнопку отправки (требует наличие микрофона)

# Тестирование проекта
Инструкции для тестирования контейнеров приложения расположенным в соответствующих README:
1. [frontend](https://github.com/moevm/mse1h2024-assistant/tree/main/frontend#readme)
2. [backend + whisper](https://github.com/moevm/mse1h2024-assistant/tree/main/backend#readme)
4. [tg_bot](https://github.com/moevm/mse1h2024-assistant/tree/main/tg_bot#readme)