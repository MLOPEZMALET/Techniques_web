TODO

FRONT-END
- deux url différentes
- deux serveurs nginx différents
- session qui se ferme automatiquement
- appli dynamique et responsive: jinja2
- toutes requêtes doivent être disponibles sur front-end: formulaires

DEVELOPPEMENT
- faire des unitest
- utiliser pipenv: done
- générer requirements.txt: done

DOCUMENTATION
- mieux préciser comment on répond au besoin du client: done
- modifier les requêtes/ liens
- créer la documentation technique (fichier .sh devient .txt): done

SÉCURITÉ
- log: "la création des logs va poser un problème: log/gunicorn.log , ici c'est nginx qui crée ce
        fichier et non vous avec —acces-log"
- Rendre la BD dynamique: création et suppression d'utilisateurs, modification de mots de passe
  -->attention: il faudra implémenter ces fonctionnalités en front-end aussi
- Sécurité par tokens: JWT ou uuid (python): done
- identification en sessions: done
- Certificats HTTPS avec Certbot: essayer de l'implémenter et voir
- Demander aux autres groupes s'ils ont réussi à être en https et s'ils ont "le cadenas"

REQUÊTES
- Formater les réponses: done
- Modifier les URL: done
- faire une requête par matching (?)
- modifier la création de contribution: il ne faut pas préciser d'ID
- juste besoin de l'ID pour supprimer une contribution: done
