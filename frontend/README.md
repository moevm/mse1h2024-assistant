# assistant

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Тестирование 
1. Проект должен быть запущен по основной инструкции(для итеграционных тестов обязательно)
2. Сборка тестового контейнера: \
```docker build -f DockerfileTest . -t test```
3. Запуск тестового контейнера \
Windows: \
```docker run --name test -d -e HOST_ADDR=host.docker.internal test```\
Linux : \
```docker run --name test -d -e HOST_ADDR=172.17.0.1 test```
4. Запуск юнит тестов \
```docker exec -it test npm run unit_test```
5. Запуск интеграционных тестов \
 ```docker exec -it test npm run integration_test```

Или запуск напрямую при наличии npm \
```npm run integration_test``` \
```npm run unit_test```


### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
