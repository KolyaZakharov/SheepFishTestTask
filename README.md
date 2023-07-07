### `git clone https://github.com/Kitazuka/SheepFish_test.git`
###  `python -m venv venv`
### `venv\Scripts\activate # on Windows`
### `source venv/bin/activate # on macOS`
### `pip install -r requirements.txt`


### create .env file

### `docker-compose up --build`
### `python manage.py migrate`
### `python manage.py loaddata printers_fixtures.json`
### `python manage.py createsuperuser`
### `celery -A SheepFish_test worker -l info -P gevent`
### `celery -A SheepFish_test beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`
