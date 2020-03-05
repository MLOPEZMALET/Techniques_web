TODO

FRONT-END
- crypter données (ssl): afala
- logout automatique: lili
- SSL certificat: afala ->desactiver certificats dans navigateur, envoyer code nginx et certificats, pb de génération du certificat. 
- deux serveurs nginx différents + deux url différentes: afala
- appli dynamique et responsive: jinja2 Mélanie
- faire les pages html/css Maëva
- librairie request: melanie
- toutes requêtes doivent être disponibles sur front-end: formulaires Maëva
- log: "la création des logs va poser un problème: log/gunicorn.log , ici c'est nginx qui crée ce
        fichier et non vous avec —acces-log": afala
- modifier doc
- fichier bash qui lance tout
- doc technique pour l'installation (revoir doc txt)
- faire une requête par matching (?): retrouver information meme si pas exact.
- modifier la création de contribution: il ne faut pas préciser d'ID
- installer brew et essayer pour le certificat: melanie

DEVELOPPEMENT
- faire des unitest ( backend ++): lili
- utiliser pipenv: done
- générer requirements.txt: done

DOCUMENTATION
- mieux préciser comment on répond au besoin du client: done

SÉCURITÉ

- Rendre la BD dynamique: création et suppression d'utilisateurs, modification de mots de passe
  -->attention: il faudra implémenter ces fonctionnalités en front-end aussi
- Sécurité par tokens: JWT ou uuid (python): done
- identification en sessions: done

REQUÊTES
- Formater les réponses: done
- Modifier les URL: done
- juste besoin de l'ID pour supprimer une contribution: done
