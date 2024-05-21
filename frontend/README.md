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

### Integration tests 
1) Выполнить 
```run.sh```
2) Собрать конейнер 
```docker build -f DockerfileTest . -t test```
3) Запустить контейнер```docker run test```
##### Или запуск напрямую при наличии npm (предварительно перейти в папку frontend)
```
npm run integration_test
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
