FROM python:3.8-slim

# install dependencies
COPY /deploy/backend/requirements.txt .
RUN pip3 install -r requirements.txt

# copy files 
COPY /backend ./backend
WORKDIR /backend

# set variables
RUN export PORT=8080
CMD exec gunicorn main:app --workers 1 --threads 4 --bind :8080 -k uvicorn.workers.UvicornWorker
