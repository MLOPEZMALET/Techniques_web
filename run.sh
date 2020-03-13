#!/bin/bash

cd ..
sudo mv ceptyconsultant.local /var/

# SUPERVISOR
sudo mv conf/supervisor/api.conf /etc/supervisor/conf.d/
sudo mv conf/supervisor/app_front.conf /etc/supervisor/conf.d/


# NGINX
sudo mv conf/ssl/private/cepty_back.key /etc/ssl/private/
sudo mv conf/ssl/private/cepty_front.key /etc/ssl/private/
sudo mv conf/ssl/certs/cepty_back.crt /etc/ssl/certs/
sudo mv conf/ssl/certs/cepty_front.crt /etc/ssl/certs/

sudo mv conf/dhparam.pem /etc/nginx/

sudo mv conf/snippets/selfsigned_front.conf /etc/nginx/snippets/
sudo mv conf/snippets/selfsigned_back.conf /etc/nginx/snippets/
sudo mv ssl-params.conf /etc/nginx/snippets/

sudo mv conf/cepty_back.conf /etc/nginx/sites-available/ 
sudo mv conf/cepty_front.conf /etc/nginx/sites-available/ 

ln -s /etc/nginx/sites-available/cepty_back.conf /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/cepty_front.conf /etc/nginx/sites-enabled/

cd /var/ceptyconsultant.local

sudo python3.7 -m pipenv install -r requirements.txt
sudo python3.7 -m pipenv shell

sudo supervisorctl reread
sudo supervisorctl restart all

