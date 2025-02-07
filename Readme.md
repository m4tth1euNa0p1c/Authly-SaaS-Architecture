```markdown
# Authly SaaS Architecture

Une plateforme d’authentification et d’autorisation complète, basée sur FastAPI et Firebase côté back-end, et sur React (Vite + TypeScript) côté front-end.

---

## Aperçu

Cette architecture propose :
- Authentification JWT avec expiration
- Hash sécurisée des mots de passe via bcrypt
- Vérification d’adresse email via Firebase
- Protection de routes pour contrôler l’accès aux sections sensibles

Le tout suit les meilleures pratiques de sécurité et vise évolutivité et maintenance.

---

## Structure du Projet

```
Authly-SaaS-Architecture/
├── api/
│   ├── app/
│   │   ├── config/          # Fichiers de configuration
│   │   ├── core/            # Base de données, Firebase, sécurité, utilitaires
│   │   ├── middleware/      # Middlewares (CORS, limitation de débit, etc.)
│   │   ├── models/          # Modèles (User, RefreshToken, etc.)
│   │   ├── repositories/    # Opérations CRUD
│   │   ├── routes/          # Endpoints API
│   │   ├── schemas/         # Schémas Pydantic
│   │   └── services/        # Logique de gestion (authentification, utilisateurs)
│   ├── credentials/         # Fichiers d’identifiants Firebase
│   ├── migrations/          # Fichiers de migration Alembic
│   ├── requirements.txt     # Dépendances Python
│   └── tests/               # Tests API
├── db/                      # Configuration base de données et fichiers Docker
└── frontend/
   ├── public/               # Ressources publiques (HTML, images)
   ├── src/
   │   ├── assets/
   │   ├── components/
   │   ├── contexts/
   │   ├── hooks/
   │   ├── layouts/
   │   ├── pages/
   │   ├── services/
   │   ├── store/
   │   └── utils/
   ├── package.json
   └── vite.config.ts
```

---

## Comment Exécuter le Projet

### Back-End (API)

1. Créer un fichier `.env` dans `api` :
   ```env
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   DATABASE_URL=postgresql://authly_user:SuperSecurePassword123!@localhost:5432/authly_db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   FIREBASE_SERVICE_ACCOUNT_PATH=credentials/authly-saas-architecture-firebase-adminsdk-fbsvc-76317ba7c3.json
   API_BASE_URL=http://127.0.0.1:8000
   ```

2. Installer les dépendances :
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. Lancer l’API :
   ```bash
   uvicorn app.main:app --reload
   ```

### Front-End (React)

1. Créer le fichier `.env` dans `frontend` :
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000
   VITE_FIREBASE_API_KEY=your_firebase_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
   VITE_FIREBASE_PROJECT_ID=your_firebase_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
   VITE_FIREBASE_APP_ID=your_firebase_app_id
   VITE_FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id
   ```

2. Installer les dépendances :
   ```bash
   cd frontend
   npm install
   ```

3. Lancer le front-end :
   ```bash
   npm run dev
   ```

---

## Améliorations Futures

- Gestion avancée des tokens (refresh token, liste noire, rotation de clés)
- Validation d’entrée approfondie (normaliser emails, mots de passe robustes)
- Journalisation et gestion d’erreurs structurées (framework de logging, intégration Sentry)
- Limitation de débit (IP-based rate limiting)
- Stockage de tokens plus sécurisé (cookies HTTP-only)
- Couverture de tests améliorée (pytest, Jest) et pipelines CI/CD
- Audits de sécurité réguliers pour respecter les bonnes pratiques
```
