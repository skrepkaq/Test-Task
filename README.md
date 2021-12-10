# Test task
Используется Django фреймворк и SQlite
## Установка
1. Создайте и активируйте [venv](https://docs.python.org/3/library/venv.html)
2. Используя [pip](https://pip.pypa.io/en/stable/) установите библиотеки из **requirements.txt**.
```bash
pip install -r requirements.txt
```
3. Мигрируйте базу данных с помощью файла **manage.py** из директории **src**
```bash
python manage.py makemigrations
python manage.py migrate
```

## Использование

1. Добавьте типы оборудования
2. Запустите сервер:
```bash
python manage.py runserver
```
3. Зайдите на [http://localhost:8000](http://localhost:8000)