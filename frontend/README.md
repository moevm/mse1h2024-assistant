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

### Unit tests (Для запуска тестов нужно перейти в папку frontend)
```
npm run unit_test
```

### Tests 
1) Выполнить ```run.sh``` (для итеграционных тестов обязательно)
2) Собрать конейнер ```docker build -f DockerfileTest . -t test```
3) Запустить контейнер ```docker run --name test -d test```
4) Запустить юнит тесты ```docker exec -it test npm run unit_test```
5) Запустить интеграционные тесты ```docker exec -it test npm run integration_test```
##### Или запуск напрямую при наличии npm (предварительно перейти в папку frontend)
```npm run integration_test```
```npm run unit_test```


### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
