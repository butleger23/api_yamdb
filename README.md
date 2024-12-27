### Описание проекта:

Данный проект создает REST API для работы с YaTube.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/butleger23/api_final_yatube.git
```

```
cd api_final_yatube
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
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов при запуске на локальном сервере:

```
http://127.0.0.1:8000/api/v1/posts/ - Получить список всех публикаций
```
```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/ - Получение комментария к публикации по id.
```
```
http://127.0.0.1:8000/api/v1/follow/ - Подписка пользователя от имени которого сделан запрос на пользователя переданного в теле запроса
```