### Описание проекта:

Данный проект создает REST API для работы с YaMDB.

### Авторы проекта:

Данный проект был разработан Королевым Владимиром, Максименко Стефаном и Полывяным Артемом

### Использованные технологии:

В данном проекте используются данные технологии:

[Django](https://www.djangoproject.com/)

[Django rest framework](https://www.django-rest-framework.org/)

[DRF SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

[DRF nested routers](https://github.com/alanjds/drf-nested-routers)

[python-dotenv](https://pypi.org/project/python-dotenv/)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:butleger23/api_yamdb.git
```

```
cd api_final_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate --run-syncdb
```

Запустить проект:

```
python3 manage.py runserver
```
### Как наполнить датабазу из файлов csv:

Находясь в api_final_yamdb/api_final_yamdb, выполнить команду:
```
python3 manage.py import_data
```
### Документация по API:

После запуска проекта документацию можно найти по url:
```
http://127.0.0.1:8000/redoc/
```
### Для получения кода подтверждения по email:

Необходимо в директории api_yamdb/api_yamdb создать файл .env в котором создать две переменных:
1) host_email - ваш email
2) app_password - app_password, созданный вами согласно данному гайду https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=ru

Альтернативно, можно изменить в settings.py
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
на
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
и получать confirmation_code таким образом