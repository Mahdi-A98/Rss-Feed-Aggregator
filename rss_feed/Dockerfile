FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext
COPY . /code/

EXPOSE 8000

CMD python manage.py makemessages --all && \
    python manage.py compilemessages && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000