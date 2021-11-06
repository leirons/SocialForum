# Forum like 2ch

### Что реализовано
```
* Бан матерящих пользователей
* Регистрация/Авторизация
* Отправка логов на емайл с использованием Celery/Redis
* Лайки сообщений/тем
* Добавление/Удаление постов
* Добавление/Удаление комментариев
* Популярность постов
* Онлайн/Оффлайн пользователя, последний раз когда был замечен на сайте
```



### Установка
```
git clone https://github.com/leirons/Forum.git
cd board/
python -m spacy download en
python manage.py load_country
pip install -r requirements.txt # Перед командой активировать виртуальное окружение

MAILCHIMP_API_KEY = "YOUR KEY"
MAILCHIMP_DATA_CENTER = "YOUR DATA"
MAILCHIMP_EMAIL_LIST_ID = "YOUR LIST ID"

python manage.py makemigrations
python manage.py migrate
```


### Запуск
```
python manage.py runserver
```

### Cоздание администратора
```
python manage.py createsuperuser
```

### Docker
```
docker-compose up
```

### Запуск очереди заданий
```
celery -A board beat 
celery -A board worker -l INFO --pool=solo
```

### Python 3.8
```
profanity_filter
```

