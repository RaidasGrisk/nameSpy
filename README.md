# setup

``` bash
docker build -t social_score -f deploy/social_score/Dockerfile .
docker run -p 8080:8080 social_score:latest

docker build -t job_title -f deploy/job_title/Dockerfile .
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
docker build -f deploy/social_score/Dockerfile . --tag gcr.io/namesapi-1581010760883/socialscore
docker push gcr.io/namesapi-1581010760883/socialscore

gcloud run deploy --image gcr.io/namesapi-1581010760883/socialscore
gcloud run services update socialscore --memory 512

####
docker build -f deploy/job_title/Dockerfile . --tag gcr.io/namesapi-1581010760883/jobtitle
docker push gcr.io/namesapi-1581010760883/jobtitle

gcloud run deploy --image gcr.io/namesapi-1581010760883/jobtitle
gcloud run services update jobtitle --memory 2G

###
# https://cloud.google.com/compute/docs/machine-types
# https://vinta.ws/code/the-complete-guide-to-google-kubernetes-engine-gke.html
gcloud container clusters create jobtitle-cluster --machine-type=n1-standard-2 --region=us-central1-c
kubectl apply -f deploy/job_title/app.yaml

# Manually expose the pod 80 to 8080
# 80	31508	8080	TCP

```

``` bash
kubectl get pods
kubectl get services

```

# WEBSITE

https://medium.com/google-cloud/a-clearer-vue-in-google-cloud-2370a4b048cd

``` bash
docker build -t vue_app -f deploy/web/Dockerfile .
docker run -p 8080:8080 vue_app


# set the current project id
PROJECT_ID=$(gcloud config get-value core/project)
echo $PROJECT_ID # just so you know which project you're pushing to
# configure gcloud docker auth, if this hasn't been configured
gcloud auth configure-docker
# create a tag
docker tag vue_app gcr.io/$PROJECT_ID/vue-app:v1
# enable the containerregistry.googleapis.com service
gcloud services enable containerregistry.googleapis.com
# push our docker image to gcr.io
docker push gcr.io/$PROJECT_ID/vue-app:v1


# set the current project id
PROJECT_ID=$(gcloud config get-value core/project)
# create a new service account to be run with the VM
SA_NAME="vue-app-sa"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
gcloud iam service-accounts create $SA_NAME \
 --display-name $SA_NAME \
 --project $PROJECT_ID
# we will need a FW rule to expose tcp:8080
gcloud compute firewall-rules create vue-fw --allow tcp:8080,icmp
# grant the default compute service account view permission to the project to pull the gcr.io image
gcloud projects add-iam-policy-binding $PROJECT_ID \
 --member=serviceAccount:$SA_EMAIL \
 --role='roles/viewer'
# create the VM with create-with-container
gcloud compute instances create-with-container vue-app-vm \
 --container-image=gcr.io/$PROJECT_ID/vue-app:v1 \
 --service-account=$SA_EMAIL \
 --machine-type=f1-micro \
 --scopes=https://www.googleapis.com/auth/cloud-platform \
 --zone us-west1-a
# to see the VMs in our project
gcloud compute instances list
# get the external ip
EXTERNAL_IP=$(gcloud compute instances list --format="get(networkInterfaces[0].accessConfigs[0].natIP)" --filter="name='vue-app-vm'")
# in your browser, navigate to the echoed address.  NOTE: the deployment may take about a minute.
echo http://$EXTERNAL_IP:8080

# update VM instance with new image
gcloud compute instances update-container --container-image=gcr.io/namesapi-1581010760883/vue-app vue-app-vm

# cleanup
gcloud compute firewall-rules delete vue-fw
gcloud compute instances delete vue-app-vm --zone=us-west1-a
gcloud iam service-accounts delete $SA_EMAIL

```
