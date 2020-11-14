#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the main directory of the project
docker build -f deploy/web_score/Dockerfile . --tag gcr.io/namesapi-1581010760883/webscore
docker push gcr.io/namesapi-1581010760883/webscore

gcloud config set project namesapi-1581010760883
gcloud run deploy \
  --image gcr.io/namesapi-1581010760883/webscore \
  --platform managed \
  --region europe-north1 \
  --memory 2G \
  --max-instances 5 \
  --timeout 60
