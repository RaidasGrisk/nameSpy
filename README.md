# setup

``` bash
docker build -t social_score -f api_build/social_score/Dockerfile .
docker run -p 8080:8080 social_score:latest

docker build -t job_title -f api_build/job_title/Dockerfile .
docker run -p 8080:8080 job_title:latest

```

``` bash
docker image ls
docker container ls
docker system prune -a --volumes

gcloud container images list
```


``` bash

# https://cloud.google.com/run/docs/building/containers
gcloud auth configure-docker
docker build -f api_build/social_score/Dockerfile . --tag gcr.io/namesapi-1581010760883/socialscore
docker push gcr.io/namesapi-1581010760883/socialscore

gcloud run deploy --image gcr.io/namesapi-1581010760883/socialscore
gcloud run services update socialscore --memory 512

####
docker build -f api_build/job_title/Dockerfile . --tag gcr.io/namesapi-1581010760883/jobtitle
docker push gcr.io/namesapi-1581010760883/jobtitle

gcloud run deploy --image gcr.io/namesapi-1581010760883/jobtitle
gcloud run services update gcr.io/namesapi-1581010760883/jobtitle  --memory 2560

###
# https://cloud.google.com/compute/docs/machine-types
# https://vinta.ws/code/the-complete-guide-to-google-kubernetes-engine-gke.html
gcloud container clusters create jobtitle-cluster --machine-type=n1-standard-2 --region=us-central1-c
kubectl apply -f api_build/job_title/app.yaml

# Manually expose the pod 80 to 8080
# 80	31508	8080	TCP

```

``` bash
kubectl get pods
kubectl get services

```
