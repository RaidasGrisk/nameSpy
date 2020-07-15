#!/bin/bash

# execute this to build and deploy the image to google cloud run
# execute this from the msain directory of the project
docker build -f deploy/gateway/Dockerfile . --tag gcr.io/namesapi-1581010760883/gateway
docker push gcr.io/namesapi-1581010760883/gateway
gcloud run deploy --image gcr.io/namesapi-1581010760883/gateway --platform managed --region europe-north1
