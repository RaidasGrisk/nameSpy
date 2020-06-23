FROM python:3.7-slim

# install dependencies
COPY /deploy/gateway/requirements.txt .
RUN pip3 install -r requirements.txt

# copy files
COPY /gateway ./gateway
WORKDIR /gateway

# set variables
RUN export PORT=8080
CMD exec gunicorn --bind :8080 --workers 1 --threads 4 main:app
