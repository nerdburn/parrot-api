# Parrot API

## Installation

Clone repo:
```
git clone https://github.com/nerdburn/parrot-api.git
cd parrot-api
```

Create and activate local python environment:
```
virtualenv -p python3 env
. ./env/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
pip freeze > requirements.txt
```

Save local environment variables:

```
mv env.template .env
```

Create database:
```
createdb parrot
```

Django setup:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```
