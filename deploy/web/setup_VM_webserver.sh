# https://www.cloudbooklet.com/install-web-apps-with-ssl-certificate-on-google-cloud-platform/

# update
sudo apt update
sudo apt install nginx
sudo apt install nano

sudo apt-get install ufw
udo ufw allow 'Nginx Full'

# check if can access the server from explorer
# goto the IP adress of the server to see index.html
sudo systemctl status nginx

# change permissions to be able to write to root
sudo chmod /var/www/html/

# transfer the site build to the server
gcloud compute scp --recurse web/dist/* web-server:/var/www/html

# edit the location of index.html in nginx config
sudo nano /etc/nginx/sites-available/default

# setup certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx certonly

# update nginx config at /etc/nginx/sites-available/default
#
# server {
#     listen [::]:80;
#     listen 80;
#
#     server_name namespy.dev www.namespy.dev;
#     # redirect http to https www
#     return 301 https://www.namespy.dev$request_uri;
# }
#
# server {
#     listen [::]:443 ssl http2;
#     listen 443 ssl http2;
#
#     server_name namespy.dev;
#
#     ssl_certificate /etc/letsencrypt/live/namespy.dev/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/namespy.dev/privkey.pem;
#
#     root /var/www/html;
#     index index.html;
#
#     # redirect https non-www to https www
#     return 301 https://www.namespy.dev$request_uri;
# }
#
# server {
#     listen [::]:443 ssl http2;
#     listen 443 ssl http2;
#
#     server_name www.namespy.dev;
#
#     ssl_certificate /etc/letsencrypt/live/namespy.dev/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/namespy.dev/privkey.pem;
#
#     error_log /home/mrraidas/error.log;
#
#     root /var/www/html;
#     index index.html;
#
#     location / {
#         try_files $uri $uri/ /index.php?$args;
#     }
#
#     location ~ \.php$ {
#         try_files $uri =404;
#         fastcgi_split_path_info ^(.+\.php)(/.+)$;
#         fastcgi_pass unix:/run/php/php7.2-fpm.sock;
#         fastcgi_index index.php;
#         include fastcgi_params;
#
#         add_header Content-Security-Policy "img-src * 'self' data: blob: https:; default-src 'self' https://*.googleapis.com https://*.googletagmanager.com https://*.google-analytics.com https://s.ytimg.com https://www.youtube.com https://www.namespy.dev https://*.googleapis.com https://*.gstatic.com https://*.gravatar.com https://*.w.org data: 'unsafe-inline' 'unsafe-eval';" always;
#         add_header X-Xss-Protection "1; mode=block" always;
#         add_header X-Frame-Options "SAMEORIGIN" always;
#         add_header X-Content-Type-Options "nosniff" always;
#         add_header Access-Control-Allow-Origin "https://www.namespy.dev";
#         add_header Referrer-Policy "origin-when-cross-origin" always;
#         add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload";
#     }
# }

sudo nginx -t
sudo service nginx restart
