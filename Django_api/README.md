# instruction
```bash
pip install django
pip install djangorestframework

django-admin startproject some
cd some
django-admin startapp api 
```

Update settings.py:

```python
INSTALLED_APPS = (
	...
	'api',
	'rest_framework',
)
```

And replace the files :

```bash
./urls.py
./api/models.py
./api/urls.py
./api/views.py
```

then commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
