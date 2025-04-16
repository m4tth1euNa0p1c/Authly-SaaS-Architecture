solution dédiée à l'authentification et à l'autorisation.
Structure du Projet
 * api/ : Composant serveur (Back-end) développé avec FastAPI.
 * db/ : Configuration de la base de données et fichiers de configuration Docker.
 * frontend/ : Interface utilisateur (Front-end) développée avec React, utilisant Vite et TypeScript.
Installation
Composant Serveur (API)
 * Configuration de l'environnement : Dans le répertoire api, créez un fichier .env et définissez les variables d'environnement requises (par exemple : HOST, PORT, DATABASE_URL).
 * Installation des dépendances :
   cd api
pip install -r requirements.txt

 * Démarrage du serveur API :
   uvicorn app.main:app --reload

Interface Utilisateur (Front-End)
 * Configuration de l'environnement : Dans le répertoire frontend, créez un fichier .env et renseignez les variables d'environnement nécessaires.
 * Installation des dépendances :
   cd frontend
npm install

 * Lancement de l'application front-end :
   npm run dev

Feuille de Route
 * Amélioration de la gestion des jetons de rafraîchissement.
 * Renforcement de la validation et de la sécurité des données entrantes.
 * Implémentation de la journalisation, de la limitation de débit et d'une gestion avancée des erreurs.
 * Optimisation du stockage sécurisé des jetons d'authentification.
