# Configuration et Déploiement de la Base de Données pour Authly

Ce dossier contient toute la configuration nécessaire pour déployer et gérer la base de données PostgreSQL utilisée par l'application Authly en production.

## Structure du Dossier

- **docker/**
  - **Dockerfile** : Fichier de configuration pour construire une image Docker PostgreSQL personnalisée.
  - **init.sql** : Script d'initialisation de la base de données (création du schéma, tables, triggers, etc.).

- **alembic/**
  - **env.py** : Configuration d'Alembic pour la gestion des migrations.
  - **script.py.mako** : Template utilisé par Alembic pour générer des scripts de migration.
  - **versions/** : Dossier où seront stockées les migrations générées.

- **config/**
  - **database.ini** : Fichier de configuration contenant la chaîne de connexion à la base de données, utilisé par Alembic.

## Instructions de Déploiement

1. **Conteneurisation de la Base de Données :**

   Pour construire et lancer le conteneur PostgreSQL, utilisez la commande suivante depuis le dossier `db/docker` (ou via Docker Compose en production) :

   ```bash
   docker build -t authly-db .
   docker run --name authly-db -p 5432:5432 -d authly-db
   ```

2. **Migrations de la Base de Données :**

   - Initialisez Alembic (si ce n'est pas déjà fait) :
     ```bash
     alembic init alembic
     ```
   - Configurez le fichier `alembic.ini` ou `db/config/database.ini` avec votre chaîne de connexion.
   - Pour générer une migration :
     ```bash
     alembic revision --autogenerate -m "Initial migration"
     ```
   - Pour appliquer les migrations :
     ```bash
     alembic upgrade head
     ```

3. **Variables Sensibles :**

   Les informations sensibles (telles que les mots de passe et chaînes de connexion) doivent être gérées via des fichiers `.env` ou un service de gestion de secrets en production.

Voici une réponse en deux parties :

---

## 1. Rôle des Variables d'Environnement dans le Dockerfile

Les variables définies dans votre Dockerfile pour PostgreSQL jouent un rôle essentiel lors du démarrage du conteneur. En particulier :

- **`ENV POSTGRES_USER=authly_user`**  
  Définit le nom de l'utilisateur par défaut qui sera créé dans la base de données PostgreSQL au démarrage du conteneur. Cet utilisateur sera utilisé pour se connecter à la base de données via votre application.

- **`ENV POSTGRES_PASSWORD=SuperSecurePassword123!`**  
  Définit le mot de passe pour l'utilisateur par défaut (`authly_user`). Ce mot de passe est requis pour les connexions à la base de données et doit être stocké de manière sécurisée (dans un environnement de production, il est recommandé d'utiliser un gestionnaire de secrets ou de l'injecter via Docker Compose).

- **`ENV POSTGRES_DB=authly_db`**  
  Indique le nom de la base de données qui sera créée automatiquement lors du démarrage du conteneur. Cette base sera la base par défaut sur laquelle votre application fonctionnera.

Ces variables permettent donc à l'image officielle de PostgreSQL de configurer une instance prête à l'emploi avec un utilisateur, un mot de passe et une base de données spécifiés, facilitant ainsi la connexion depuis votre API et la gestion centralisée des données.

---

## 2. Étapes et Commandes à Réaliser pour Continuer

### A. Construction et Lancement du Conteneur PostgreSQL

1. **Ouvrir un terminal (PowerShell ou WSL Ubuntu)**  
   Assurez-vous de vous placer dans le dossier `db/docker` où se trouve votre Dockerfile.

2. **Construire l'image Docker**  
   Utilisez la commande suivante pour construire l'image :
   ```bash
   docker build -t authly-db .
   ```
   - **Explication** :  
     - `-t authly-db` donne le nom `authly-db` à l'image construite.
     - Le point `.` indique que le Dockerfile se trouve dans le répertoire courant.

3. **Lancer un conteneur à partir de l'image**  
   Utilisez la commande suivante pour lancer le conteneur PostgreSQL :
   ```bash
   docker run --name authly-db -p 5432:5432 -d authly-db
   ```
   - **Explication** :  
     - `--name authly-db` nomme le conteneur.
     - `-p 5432:5432` expose le port 5432 du conteneur sur le port 5432 de votre machine (port standard de PostgreSQL).
     - `-d` lance le conteneur en mode détaché.
     - `authly-db` est le nom de l'image que vous avez construite.

4. **Vérifier que le conteneur fonctionne**  
   Vous pouvez exécuter :
   ```bash
   docker ps
   ```
   pour lister les conteneurs en cours d'exécution, ou regarder les logs avec :
   ```bash
   docker logs authly-db
   ```

---

### B. Tester la Connexion à la Base de Données via le Script Python

1. **Assurez-vous que votre base de données est accessible**  
   Dans votre fichier `.env` (situé dans le dossier `api` par exemple), la variable `DATABASE_URL` doit être configurée pour pointer vers la base de données dans le conteneur.  
   Par exemple, pour un environnement de développement local, vous pourriez avoir :
   ```dotenv
   DATABASE_URL=postgresql://authly_user:SuperSecurePassword123!@localhost:5432/authly_db
   ```

2. **Exécuter le script de test**  
   Dans un terminal (PowerShell ou WSL) et depuis le dossier racine de votre projet (ou le dossier `api`), lancez le script de test pour vérifier la connexion :
   ```bash
   python -m api.tests.test_db_connection
   ```
   - **Ce script** établit une connexion via SQLAlchemy et exécute une simple requête `SELECT 1`.  
   - Le script affichera un message de succès si la connexion est établie, ou une erreur détaillée si quelque chose ne va pas.

---

### C. Récapitulatif des Commandes à Exécuter

1. **Construction de l'image Docker :**
   ```bash
   cd db/docker
   docker build -t authly-db .
   ```
2. **Lancement du conteneur PostgreSQL :**
   ```bash
   docker run --name authly-db -p 5432:5432 -d authly-db
   ```
3. **Vérification du conteneur en cours d'exécution :**
   ```bash
   docker ps
   docker logs authly-db
   ```
4. **Vérification de la connexion à la DB via le script Python :**
   ```bash
   cd ../..   # revenir à la racine du projet ou au dossier 'api'
   python -m api.tests.test_db_connection
   ```
---

Ces étapes vous permettent de construire, lancer et tester la base de données conteneurisée, tout en vous assurant que la configuration et la connectivité fonctionnent comme prévu en production.

## Récapitulatif de l'Architecture du Dossier **db**

```
db/
├── README.md                     # Documentation de la configuration et du déploiement
├── alembic
│   ├── env.py                    # Configuration Alembic pour les migrations
│   ├── script.py.mako            # Template pour les scripts de migration
│   └── versions/                 # Dossier pour stocker les fichiers de migration générés
├── config
│   └── database.ini              # Fichier de configuration pour la chaîne de connexion
└── docker
    ├── Dockerfile                # Dockerfile pour construire l'image PostgreSQL personnalisée
    └── init.sql                  # Script d'initialisation SQL pour la base de données
```

---