FROM python:3.7-slim

# install dependencies
COPY /deploy/social_score/requirements.txt ./api/

RUN pip install -r api/requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download lt_core_news_sm

# install and configure tor
RUN apt update && \
    apt install tor -y
RUN pip install requests[socks]  # somehow putting this inside requirements is not enough

# setup tor config
# RUN tor_password=`grep 'tor_password' private.py | cut -f 2 -d "'"`
RUN echo HashedControlPassword $(tor --hash-password "kjhadfjkasf12a32sf456" | tail -n 1) >> /etc/tor/torrc
RUN echo "ControlPort 9051" >> /etc/tor/torrc

# copy files
COPY /api/data_sources ./api/data_sources/
COPY /api/web_score ./api/web_score/
COPY /api/proxy ./api/proxy/
COPY /api/__init__.py /api/globals.py /api/helpers.py /api/private.py ./api/
COPY /api/endpoint_get_social_score.py ./api/

# set variables
EXPOSE 9050 9051
RUN export PORT=8080

# launch app
WORKDIR /api
CMD service tor stop && \
    service tor start && \
    exec gunicorn --bind :8080 --workers 1 --threads 4 endpoint_get_social_score:app
