#!/bin/bash

# Creating dynamic user
if ! whoami 2>&1 &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${HOME}:/sbin/nologin" >> /etc/passwd
  fi
fi

cd /app

export FLASK_APP=simplesurveyapp.py

flask run --host=0.0.0.0

