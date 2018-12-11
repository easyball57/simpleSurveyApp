#!/bin/bash

docker build -t registry2.apps.ocp.lab-nxtit.com/simplesurveyapp/ssa:latest -f Dockerfile .

docker login -u easyball57 -p $(oc whoami -t) registry2.apps.ocp.lab-nxtit.com

docker push registry2.apps.ocp.lab-nxtit.com/simplesurveyapp/ssa:latest

