# Event Manager API Projekt

# Abhängigkeiten installieren
- pip-compile requirements.in
- pip-compile requirements-dev.in
- pip-sync requirements.txt requirements-dev.txt


# Zugang
- account: admin2
- passwort: abcd1234

## API Token
- curl -d "username=bob&password=abcd1234!" http://127.0.0.1:8000/api/token

### Alle Objekte (ohne Permissions)
- curl  http://127.0.0.1:8000/api/event/ 

### Create Objekte (mit Token)
- curl -d "name='Test-Event von Api'&min_group=5&category=33" http://127.0.0.1:8000/api/event/ -H "Authorization: Token - a1a9af22839941c31eddedbf3cc794e37a4337f4"

## Validierung
- Model-Validierung: Built-in Validators: https://docs.djangoproject.com/en/5.0/ref/validators/
- (siehe events/models.py, class Category)

- eigene Validator-Funktionen (siehe events/validators.py)
- Kreuzfeld-Prüfung (siehe events/serializers.py, Funktion validate)

## Django Restframework 
- https://www.django-rest-framework.org/
- https://django-ninja.dev/

## Django Filter
- https://django-filter.readthedocs.io/

## Model Manager
- https://docs.djangoproject.com/en/5.0/ref/models/querysets/#methods-that-return-new-querysets
- https://docs.djangoproject.com/en/5.0/ref/models/querysets/#methods-that-do-not-return-querysets

## WSGI
- https://de.wikipedia.org/wiki/Web_Server_Gateway_Interface

## Umgebungsvariablen
- https://pypi.org/project/python-dotenv/
- https://django-environ.readthedocs.io/en/latest/


## Gunicorn (Green unicorn)
- apache mod_wsgi module oder Gunicorn als Webserver nutzen
- gunicorn --bind 0.0.0.0:8080 event_manager.wsgi:application

## Django-Extensions
- https://django-extensions.readthedocs.io/en/latest/