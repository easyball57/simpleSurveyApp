#!/bin/bash

# Creating dynamic user

if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi


# Running app - to customize

cd /app

if [! -f /db/simplesurveyapp.db]; then
  cp /app/db/simplesurveyapp.db /db/simplesurveyapp.db
fi

export FLASK_APP=simplesurveyapp.py

flask run --host=0.0.0.0
