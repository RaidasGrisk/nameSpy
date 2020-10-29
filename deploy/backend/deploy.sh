#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the main directory of the project
docker build -f deploy/backend/Dockerfile . --tag gcr.io/namesapi-1581010760883/backend
docker push gcr.io/namesapi-1581010760883/backend

gcloud config set project namesapi-1581010760883
gcloud run deploy --image gcr.io/namesapi-1581010760883/backend --platform managed --region europe-north1 --max-instances 5
