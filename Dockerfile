FROM python:3
WORKDIR /app
RUN pip install gunicorn
COPY ./gunicorn.conf.py ./wsgi.py .
CMD gunicorn --config ./gunicorn.conf.py wsgi:app
