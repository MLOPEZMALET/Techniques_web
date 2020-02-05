# mise à jour d'ubuntu
sudo apt-get clean
sudo apt-get autoclean
sudo apt-get autoremove
sudo apt update
sudo apt full-upgrade

# installation de python3.7, curl et virtualenv
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7
sudo apt install curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.7 get-pip.py
sudo python3.7 -m pip install virtualenv

# création d'un dossier qui va contenir l'environnement virtuel pour notre projet
# fait dans le dossier /home
mkdir environnements
cd environnements/

# création d'un environnement virtuel virtenvTW
python3.7 -m virtualenv virtenvTW
source virtenvTW/bin/activate

# installation de flask et flask-httpAuth
python3 -m pip install flask flask_restful
python3.7 -m pip install Flask-HTTPAuth

# aller au dossier de l'application (adapter à votre machine)
cd Documents/technique_web/api_project/

# exécution de notre application flask
python3 requests_api_run.py 

# wsgi permettra l'exécution de notre applicatiob
nano wsgi.py

# installation de gunicorn
sudo apt-get update
sudo apt-get install gunicorn
python3 -m pip install gunicorn

# test
gunicorn -b 0.0.0.0:5000 --env FOO=1 --reload --thread 3 wsgi:app

# installation de supervisor
python3 -m pip install supervisor

# création du fichier de configuration pour supervisor
echo_supervisord_conf > supervisord.conf

# création du dossier qui contiendra nos fichiers .conf pour les applications
mkdir /home/username/environnements/virtenvTW/lib/python3.7/site-packages/supervisor/conf.d/

# création du fichier .conf pour notre application (il se trouve dans notre archive)
touch /home/username/environnements/virtenvTW/lib/python3.7/site-packages/supervisor/conf.d/api_cepty.conf
sudo nano /home/username/environnements/virtenvTW/lib/python3.7/site-packages/supervisor/conf.d/api_cepty.conf

# création des fichiers log pour notre application
> log/gunicorn.log
> log/gunicorn.err.log

# configuration de supervisor à partir du fichier de configuration
supervisord -c supervisord.conf

# pour lancer supervisor
supervisord

# pour l'interprète de supervisor, permet de voir les programmes exécutés avec supervisor
supervisorctl

# installation de nginx
sudo apt-get install nginx

# ajout du nom du serveur ceptyconsultant.local et www.ceptyconsultant.local pour l'adresse 127.0.0.1 afin que le navigateur ne recherche pas en ligne
sudo nano /etc/hosts

# création du fichier conf pour notre application
sudo nano /etc/nginx/sites-available/nginx_api_cepty.conf

# activation de notre fichier conf en créant un lien vers site-enabled
sudo ln -s /etc/nginx/sites-available/nginx_api_cepty.conf /etc/nginx/sites-enabled/

# vérification des fichiers conf
sudo nginx -t

# recharger nginx
sudo service nginx restart

# sécurité

# on crée un autre fichier ou on met des configurations de sécurité pour ne pas "polluer" la configuration de nginx
sudo nano /etc/nginx/snippets/secu-params.conf
# on écrit le contenu qui se trouve dans le fichier secu-params.conf dans l'annexe

# on édite le fichier (se trouve en annexe)
sudo nano /etc/nginx/sites-available/nginx_api_cepty.conf

