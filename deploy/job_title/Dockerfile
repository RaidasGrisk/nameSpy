FROM python:3.7-slim

# installing it here as it takes most of the build time
# installing find-job-title is painful due to gcc dependencies
# https://pythonspeed.com/articles/smaller-python-docker-images/
RUN apt-get update && \
    apt-get -qq install libffi-dev gcc libc-dev g++ libc-dev libxml2 && \
    pip install acora && \
    pip install pyahocorasick && \
    pip install torch && \
    apt-get remove -y gcc && apt-get -y autoremove

RUN pip install spacy
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download lt_core_news_sm

COPY /deploy/job_title/requirements.txt .
RUN pip3 install -r requirements.txt

# install and configure tor
RUN apt update && \
    apt install tor -y
RUN pip install requests[socks]  # somehow putting this inside requirements is not enough

# copy files
COPY /api/data_sources ./api/data_sources/
COPY /api/job_titles ./api/job_titles/
COPY /api/proxy ./api/proxy
COPY /api/__init__.py /api/globals.py /api/helpers.py /api/private.py /api/endpoint_get_job_title.py ./api/

WORKDIR /api

# setup tor config
# RUN tor_password=`grep 'tor_password' private.py | cut -f 2 -d "'"`
RUN echo HashedControlPassword $(tor --hash-password "kjhadfjkasf12a32sf456" | tail -n 1) >> /etc/tor/torrc
RUN echo "ControlPort 9051" >> /etc/tor/torrc

# set variables
EXPOSE 9050 9051
RUN export PORT=8080
CMD service tor stop && \
    service tor start && \
    exec gunicorn --bind :8080 --workers 1 --threads 4 endpoint_get_job_title:app
