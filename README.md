# Library

*Library* est une application simple pour gérer sa bibliothèque. Elle inclut une gestion de la PAL (Pile à Lire), de la WishList (Liste de souhaits), des lectures en cours et plus.


**Version** : 0.1.0

## Technologies
- **IDE** : VSCode
- **Back-end** : Flask

*Library* est une application conteneuriser avec **Docker** 

## How to use ?

### Pré-requis

Avoir installé **[Docker](https://www.docker.com/)** et **[PostgreSQL](https://www.postgresql.org/)** 

### Lancer l'application

A la racine du projet (`library/`) entrez la commande suivante pour lancer le container docker : `docker-compose up -d --build`

Dans un navigateur web entré l'url suivant : http://localhost:5001/

Pour éteindre le container lancer la commande : `docker-compose down`