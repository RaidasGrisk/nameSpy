gcloud compute ssh vue-app-vm

sudo mkdir nginx-ssl
cd nginx-ssl

sudo nano docker-compose.yml

# version: "3.8"
# services:
#     web:
#         image: nginx:latest
#         restart: always
#         volumes:
#             - ./public:/var/www/html
#             - ./conf.d:/etc/nginx/conf.d
#             - ./certbot/conf:/etc/nginx/ssl
#             - ./certbot/data:/var/www/certbot
#         ports:
#             - 80:80
#             - 443:443
#
#     certbot:
#         image: certbot/certbot:latest
#         command: certonly --webroot --webroot-path=/var/www/certbot --email mrraidas@gmail.com --agree-tos --no-eff-email -d namespy.dev -d www.namespy.dev
#         volumes:
#             - ./certbot/conf:/etc/letsencrypt
#             - ./certbot/logs:/var/log/letsencrypt
#             - ./certbot/data:/var/www/certbot

sudo mkdir conf.d
sudo nano conf.d/default.conf

# server {
#     listen [::]:80;
#     listen 80;
#
#     server_name namespy.dev www.namespy.dev;
#
#     location ~ /.well-known/acme-challenge {
#         allow all;
#         root /var/www/certbot;
#     }
# }


# https://cloud.google.com/compute/docs/instances/connecting-to-instance
docker run docker/compose:1.26.2 version

docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.26.2 up -d

sudo nano conf.d/default.conf
# server {
#     listen [::]:80;
#     listen 80;
#
#     server_name namespy.dev www.namespy.dev;
#
#     location ~ /.well-known/acme-challenge {
#         allow all;
#         root /var/www/certbot;
#     }
#
#     # redirect http to https www
#     return 301 https://www.namespy.dev$request_uri;
# }
#
# server {
#     listen [::]:443;
#     listen 443;
#     ssl on;
#
#     server_name www.namespy.dev;
#
#     # SSL code
#     ssl_certificate /etc/nginx/ssl/live/namespy.dev/fullchain.pem;
#     ssl_certificate_key /etc/nginx/ssl/live/namespy.dev/privkey.pem;
#
#     root /var/www/html/;
#
#     location / {
#         index index.html;
#     }
# }

# do this from root dir of the project
# copy dist folder into the VM
gcloud compute scp --recurse web/dist vue-app-vm:/home/raidas

# move the folder into the root dir, from which the nginx is serving the web
gcloud compute ssh vue-app-vm --command="sudo rm -r /home/mrraidas/nginx-ssl/public/* && sudo mv dist/* /home/mrraidas/nginx-ssl/public"
