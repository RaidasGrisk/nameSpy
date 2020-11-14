FROM python:3.8.2-slim

# installing it here as it takes most of the build time
# installing find-job-title is painful due to gcc dependencies
# https://pythonspeed.com/articles/smaller-python-docker-images/
RUN apt-get update && \
    apt-get install -y --no-install-recommends libffi-dev gcc libc-dev g++ libc-dev libxml2 && \
    pip install --no-cache-dir acora && \
    pip install --no-cache-dir pyahocorasick && \
    apt-get remove -y libffi-dev gcc libc-dev g++ libc-dev libxml2 && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

# separately install torch, so that its size is smaller
# as compared to default flair installation
RUN pip install --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.6.0%2Bcpu-cp38-cp38-linux_x86_64.whl
RUN pip install spacy
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download lt_core_news_sm

# remove cache again
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY /deploy/job_title/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy files
COPY /api/data_sources ./api/data_sources/
COPY /api/job_titles ./api/job_titles/
COPY /api/__init__.py /api/log_config.py /api/helpers.py /api/private.py /api/endpoint_get_job_title.py ./api/

# set variables
WORKDIR /api

# https://weastur.medium.com/production-ready-gunicorn-config-b98574033e45
# lets not use threads and use workers instead to utilize timeout
CMD exec gunicorn --bind :8080 --workers 4 --threads 1 --timeout 60  endpoint_get_job_title:app
