# Library

*Library* est une application simple pour gérer sa bibliothèque. Elle inclut une gestion de la PAL (Pile à Lire), de la WishList (Liste de souhaits), des lectures en cours et plus.


**Version** : 0.1.0

## Technologies
- **IDE** : VSCode
- **Back-end** : Flask
- **Front-end** : TypeScript 

*Library* est une application conteneuriser avec **Docker** et elle utilise l'API **Open Library**

## How to use ?

### Pré-requis

Avoir installé **[Docker](https://www.docker.com/)** et **[PostgreSQL](https://www.postgresql.org/)** 

### PostgreSQL

Créer un utilisateur library-user, avec comme mot de passe ganyu
> Bientôt vous pourrez choisir le nom et le mot de passe de l'utilisateur

Créer une base de données library-db, avec comme mot de passe ganyu 
> Bientôt vous pourrez choisir le nom et le mot de passe de la base de données

### Lancer l'application

A la racine du projet (`library/`) entrez la commande suivante pour lancer le container docker : `docker-compose up -d --build`
> Attention : Pour initialiser la BD assurez vous que dans le fichier `library/.env.dev` la variable `CREATE_DB=0`

Dans un navigateur web entré l'url suivant : http://localhost:5001/

Pour éteindre le container lancer la commande : `docker-compose down`