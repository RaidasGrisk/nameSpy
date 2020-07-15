#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the main directory of the project
docker build -f deploy/job_title/Dockerfile . --tag gcr.io/namesapi-1581010760883/jobtitle
docker push gcr.io/namesapi-1581010760883/jobtitle
gcloud run deploy --image gcr.io/namesapi-1581010760883/jobtitle --platform managed --region europe-north1
gcloud run services update jobtitle --memory 2G  --platform managed --region europe-north1
