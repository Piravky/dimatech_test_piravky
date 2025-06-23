# dimatech_test_piravky

Тестовое задание на роль Python разработчик в  DimaTech Ltd 
[by piravky](https://github.com/piravky)


## Логины пароли тестовых пользователей
___
### Обычный пользователь
**email:** `user@dimatech.org`

**password:** `1qwerty`


### Администратор

**email:** `admin@dimatech.org`

**password:** `1qwerty`

## Преподготовка
в директории `backend` создать файл `.env` для хранения переменных окружения
### Пример файла `.env`

Поменять значения по своему усмотрению
```
 DB_HOST=postgres
 DB_USER=postgres
 DB_PORT=5432
 DB_PASSWORD=1qwerty
 DB_DATABASE=postgres
 DB_SIGNATURE_SIGN='gfdmhghif38yrf9ew0jkf32'
 AUTH_SECRET_KEY='qYLC6PIwmKSNeNOmkYMLqeA2RuAbF6xszkJUxQjI4kE='
 AUTH_ALGORITHM='HS256'
 AUTH_ACCESS_TOKEN_EXPIRE_MINUTES=60
 AUTH_REFRESH_TOKEN_EXPIRE_DAYS=30
```

## Запуск с помощью `Docker compose`

Для запуска docker compose необходимо создать файл `.env` для хранения переменных контейнеров

### Пример файла `.env`
Поменять значения по своему усмотрению
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1qwerty
POSTGRES_DB=postgres
```
выполнить команду `docker compose up -d`

## Запуск без `Docker compose`
находясь в папке `backend`

- `pip install poetry`
- `poetry install`
- `poetry run alembic upgrade head && poetry run python3 src/main.py`
