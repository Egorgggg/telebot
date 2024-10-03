#!/bin/bash
docker build -t pochti/healthbot:$1 .
docker push pochti/healthbot:$1
docker tag pochti/healthbot:$1 pochti/healthbot:latest
docker push pochti/healthbot:latest