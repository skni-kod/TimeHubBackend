# TimeHubBackend
Jak uruchomić TimeHubBackend (od zera):
```
python -m venv .venv
```
```
.venv/Scripts/activate.ps1
```
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```
Gdy mamy już venv:
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```