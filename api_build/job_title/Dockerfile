FROM ubuntu:18.04

# copy files
COPY /api/data_sources ./api/data_sources/
COPY /api/__init__.py /api/globals.py /api/helpers.py /api/private.py ./api/
COPY /api/job_titles ./api/job_titles/
COPY /api_build/job_title/requirements.txt ./api/
COPY /api/endpoint_get_job_title.py ./api/

# install dependencies
WORKDIR /api

RUN apt-get update && apt-get install -y wget
RUN wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
RUN apt-get update && apt-get install -y unzip
RUN unzip stanford-corenlp-full-2018-02-27.zip

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install stanfordnlp
RUN pip3 install future
RUN pip3 install googletrans
RUN pip3 install wheel

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository universe
RUN apt-get install -y python3.6-dev
RUN apt-get install -y build-essential
RUN pip3 install pyahocorasick==1.4.0
RUN pip3 install find-job-titles==0.7.0

RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download lt_core_news_sm

RUN apt install -y default-jre

# set variables
RUN export PORT=8080

# ENTRYPOINT ["python"]
# CMD ["app.py"]
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 endpoint_get_job_title:app
CMD exec gunicorn --bind :8080 --workers 1 --threads 4 endpoint_get_job_title:app
