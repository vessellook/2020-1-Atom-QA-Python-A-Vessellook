### Подготовка к первому запуску
Создать и отредактировать файл **.env**
```
cp .env_template .env
``` 
Выполнить настройки
```
scripts/install.sh
```

### Запуск
Поднять контейнеры
```
docker-compose up
```
Запустить тесты
```
# if you want to run tests outside docker
scripts/run.sh

# if you want to run tests inside docker
docker-compose -f tests.docker-compose.yml up --abort-on-container-exit
```
Посмотреть результаты
```
allure serve mount/allure-results
```
### Очистка
```
scripts/clean.sh
```