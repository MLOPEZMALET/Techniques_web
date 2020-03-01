TODO

DEVELOPPEMENT
- faire des unitest
- utiliser pipenv
- générer requirements.txt

DOCUMENTATION
- mieux préciser comment on répond au besoin du client
- modifier les requêtes/ liens
- créer la documentation technique (fichier .sh devient .txt)

SÉCURITÉ
- log: "la création des logs va poser un problème: log/gunicorn.log , ici c'est nginx qui crée ce
        fichier et non vous avec —acces-log"
- Rendre la BD dynamique: création et suppression d'utilisateurs, modification de mots de passe
  -->attention: il faudra implémenter ces fonctionnalités en front-end aussi
- Sécurité par tokens: JWT ou uuid (python)
- Certificats HTTPS avec Certbot: essayer de l'implémenter et voir
- Demander aux autres groupes s'ils ont réussi à être en https et s'ils ont "le cadenas"

REQUÊTES
- Formater les réponses: done
- Modifier les URL: done
- faire une requête par matching (?)
- modifier la création de contribution: il ne faut pas préciser d'ID
- juste besoin de l'ID pour supprimer une contribution

QUESTIONS À POSER
- Où a lieu le login? ouverture de session? supprimer @auth.login_required?
- 
