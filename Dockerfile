FROM python:3.6

RUN apt-get update

RUN apt-get install sqlite3

RUN pip install --upgrade pip

RUN pip install flask

COPY simplesurveyapp.py /app/
COPY startup.sh /app/
COPY db /app/db/
RUN mkdir /db

RUN chmod g=u /etc/passwd
RUN chmod -R 0777 /app
RUN chmod -R 0777 /db

WORKDIR /app/

EXPOSE 5000

ENTRYPOINT ["/app/startup.sh"]

USER 1001
