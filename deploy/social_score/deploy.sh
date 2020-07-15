#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the main directory of the project
docker build -f deploy/social_score/Dockerfile . --tag gcr.io/namesapi-1581010760883/socialscore
docker push gcr.io/namesapi-1581010760883/socialscore
gcloud run deploy --image gcr.io/namesapi-1581010760883/socialscore --platform managed --region europe-north1
gcloud run services update socialscore --memory 2G --platform managed --region europe-north1
