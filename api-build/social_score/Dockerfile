FROM python:3.7-slim

# copy files
COPY /api/data_sources ./api/data_sources/
COPY /api/__init__.py /api/globals.py /api/helpers.py /api/main.py /api/private.py ./api/
COPY /api/requirements.txt ./api/
COPY /api/endpoint_get_social_score.py ./api/

# install dependencies
WORKDIR /api
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download lt_core_news_sm

# set variables
RUN export PORT=8080

# ENTRYPOINT ["python"]
# CMD ["app.py"]
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 endpoint_get_social_score:app
CMD exec gunicorn --bind :8080 --workers 1 --threads 4 endpoint_get_social_score:app
