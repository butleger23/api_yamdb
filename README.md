### Описание проекта:

Данный проект создает REST API для работы с YaMDB.

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