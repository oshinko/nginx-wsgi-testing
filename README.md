# nginx-wsgi-testing

Start services.

```sh
docker-compose up
```


## Local development without Docker 

```sh
python3 -m venv .venv
. .venv/bin/activate
```

or Windows.

```dos
%LocalAppData%\Programs\Python\Python310\python -m venv .venv
.venv\Scripts\activate
```

Start server.

```sh
python wsgi.py
```
