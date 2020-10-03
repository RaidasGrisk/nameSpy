# deploy files, logic, file structure, docker.yaml files etc:
# https://dev.to/koddr/how-to-dockerize-your-static-website-with-nginx-automatic-renew-ssl-for-domain-by-certbot-and-deploy-it-to-digitalocean-4cjc

# can run make files, due to errors (?)
# lets run the scripts manually

chmod +x ./webserver/register_ssl.sh

sudo ./webserver/register_ssl.sh \
--domains "namespy.dev www.namespy.dev" \
--email mrraidas@gmail.com \
--data-path ./webserver/certbot/ \
--staging 1
