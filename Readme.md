# Authly SaaS Architecture

**Authly SaaS Architecture** est une solution complète d'authentification et d'autorisation.

## Structure du Projet

- **api/** : Back-end (FastAPI)
- **db/** : Configuration de la base de données et fichiers Docker
- **frontend/** : Front-end (React avec Vite & TypeScript)

## Installation

### Back-End (API)

1. **Configurer l'environnement :**  
   Créez un fichier `.env` dans le dossier `api` et définissez les variables nécessaires (ex. `HOST`, `PORT`, `DATABASE_URL`, etc.).

2. **Installer les dépendances :**
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. **Lancer l'API :**
   ```bash
   uvicorn app.main:app --reload
   ```

### Front-End (React)

1. **Configurer l'environnement :**  
   Créez un fichier `.env` dans le dossier `frontend` avec les variables nécessaires.

2. **Installer les dépendances :**
   ```bash
   cd frontend
   npm install
   ```

3. **Lancer le front-end :**
   ```bash
   npm run dev
   ```

## Roadmap

- Améliorer la gestion des tokens de rafraîchissement.
- Renforcer la validation et la sécurité des entrées.
- Implémenter la journalisation, le rate limiting et la gestion avancée des erreurs.
- Optimiser le stockage sécurisé des tokens.