FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .
CMD gunicorn --bind 0.0.0.0:6000 app:app
