# BlockSci API

## Install

```
# cp settings.py.example settings.py
# virtualenv -p python3 venv
# source venv/bin/activate
(venv) # pip install -r requirements.txt
(venv) # python app.py
```

## Query

```
(venv) # curl --header "Content-Type: application/json" --request GET http://localhost:8080/address/3M92sq9ssFaNbEwF47uteVKJsbw125juS7/transactions/
```
