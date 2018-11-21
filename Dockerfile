FROM python:3.6

RUN apt-get update

RUN apt-get install sqlite3

RUN pip install --upgrade pip

RUN pip install flask

COPY /db /db
COPY simpleSurveyApp.py /app
COPY startup.sh /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["startup.sh"]
