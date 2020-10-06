#!/bin/bash

# execute this deploy the website to VM
# execute this from the main directory of the project
# make sure the dist/ folder is already updated

# copy dist folder into the VM
gcloud compute scp --recurse web/dist web-server:/home/mrraidas

# move the folder into the root dir, from which the nginx is serving the web
gcloud compute ssh web-server --command="sudo rm -r /var/www/html/* && sudo mv /home/mrraidas/dist/* /var/www/html"
