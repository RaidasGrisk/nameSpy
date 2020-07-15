#!/bin/bash

# execute this deploy the website to VM
# execute this from the main directory of the project
# make sure the dist/ folder is already updated

# copy dist folder into the VM
gcloud compute scp --recurse web/dist vue-app-vm:/home/raidas

# move the folder into the root dir, from which the nginx is serving the web
gcloud compute ssh vue-app-vm --command="sudo rm -r /home/mrraidas/nginx-ssl/public/* && sudo mv dist/* /home/mrraidas/nginx-ssl/public"
