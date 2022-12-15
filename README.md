# wb_parser

Парсинг Wildberries

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT


## Деплой и запуск

#### 1. Клонируем репозиторий
#### 2. Переходим в директорию с проектом
#### 3. Даем права пользователю на все файлы проекты:
    
``` bash
sudo chown -R [user]:[user] ./
```

#### 4. Запускаем билд докер контейнеров:

```bash
./scripts/build_prod.sh
```

#### 5. Выполняем миграции:

```bash
./scripts/migrate_prod.sh
```

#### 6. Создаем суперпользователя Django:

```bash
./scripts/manage_prod.sh createsuperuser
```

#### 7. Запускаем докер контейнеры:

```bash
./scripts/up_prod.sh
```


#### 8. Чтобы посмотреть логи, нужно ввести команду (чтобы выйти - Ctrl + C):

```bash
docker-compose -f production.yml logs -f
```


### Документация по началу работы, деплою и API <a href="https://telegra.ph/Parsing-Wildberries-11-05">ТУТ!</a>



