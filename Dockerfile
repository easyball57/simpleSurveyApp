FROM python:3.6

RUN apt-get update

RUN apt-get install sqlite3

RUN pip install --upgrade pip

RUN pip install flask

COPY db /db/
COPY simplesurveyapp.py /app/
COPY startup.sh /app/

RUN chmod g=u /etc/passwd
RUN chmod -R g=u /app
RUN chmod -R g=u /db
RUN chmod ug+x /app/startup.sh
    
WORKDIR /app/

EXPOSE 5000

ENTRYPOINT ["/app/startup.sh"]

USER 1001
