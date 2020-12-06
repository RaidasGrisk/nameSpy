FROM python:3.8-slim

# install dependencies
RUN pip install spacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download lt_core_news_sm

COPY /deploy/web_score/requirements.txt ./api/
RUN pip install -r api/requirements.txt

# copy files
COPY /api/data_sources ./api/data_sources/
# COPY /api/web_score/scorers/preprocess_pipe.pkl ./api/web_score/scorers/
# COPY /api/web_score/scorers/model_pipe.pkl ./api/web_score/scorers/
COPY /api/web_score/scorers ./api/web_score/scorers/
COPY /api/web_score/__init__.py /api/web_score/make_score.py ./api/web_score/
COPY /api/__init__.py /api/helpers.py /api/private.py /api/log_config.py ./api/
COPY /api/endpoint_get_web_score.py ./api/

# launch app
WORKDIR /api

# https://weastur.medium.com/production-ready-gunicorn-config-b98574033e45
# lets not use threads and use workers instead to utilize timeout
# during my test this timeout is not working, so Im setting it together with
# gcloud run deploy command. Setting that is not working either :D
# therefore lets fall back to original w1 t4 config until I sort this out
CMD exec gunicorn --bind :8080 --workers 1 --threads 4 --timeout 60 endpoint_get_web_score:app
