#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the main directory of the project
docker build -f deploy/gateway/Dockerfile . --tag gcr.io/namesapi-1581010760883/namespy-api
docker push gcr.io/namesapi-1581010760883/namespy-api
gcloud run deploy --image gcr.io/namesapi-1581010760883/namespy-api --platform managed --region europe-north1 --max-instances 5
