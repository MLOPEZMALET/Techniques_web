#pour installer pipenv
python3 -m pip install pipenv 

#pour tester si c'est bon -> pipenv, version 2018.11.26
python3 -m pipenv --version 

#se placer dans le dossier du projet avant d'effectuer cette commande qui crée l'environnement virtuel
python3 -m pipenv install

#pour lancer l'environnement virtuel (pas besoin de se déplacer)
python3 -m pipenv shell

#il faut ré-installer pipenv dans cet environnement virtuel
python3 -m pip install pipenv

#pour installer un environnement virtuel à partir d'un Pipfile fourni (modifier la version de python si besoin)
python3 -m pipenv install --dev


# OU LE CREER DE TOUTES PIECES AVEC LES COMMANDES SUIVANTES:


#installation de tous les modules/librairies -> un Pipfile.lock et un Pipfile se créent
python3 -m pipenv install Flask
python3 -m pipenv install Flask-Compress
python3 -m pipenv install Flask-Cors
python3 -m pipenv install Flask-HTTPAuth
python3 -m pipenv install Flask-RESTful
python3 -m pipenv install gunicorn
python3 -m pipenv install supervisor

#pour lock l'environnement virtuel (pour ne pas que quelqu'un puisse le modifier
python3 -m pipenv lock

#pour visualiser les modules/librairies installées et mettre ça dans un requirements.txt
pip freeze > requirements.txt