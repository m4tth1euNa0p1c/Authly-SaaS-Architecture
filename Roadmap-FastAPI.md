## I. Roadmap et Checklist des Endpoints

### A. Endpoints d’Authentification  
- **Endpoints à implémenter :**  
  - **POST `/auth/login`**  
    - Valider les identifiants ou le code OAuth.
    - Vérifier le token Firebase.
    - Synchroniser l’utilisateur en base (créer ou mettre à jour).
    - Générer et retourner un JWT et, éventuellement, un refresh token.
  - **POST `/auth/logout`**  
    - Invalider le token courant.
    - Optionnel : Mettre à jour l’état du refresh token.
  - **POST `/auth/refresh`**  
    - Valider le refresh token.
    - Générer un nouveau JWT.
  - **GET `/auth/oauth/{provider}`**  
    - Rediriger vers le flux OAuth du provider (Google, GitHub, Facebook).
    - Gérer la callback côté client pour récupérer le code OAuth et finaliser l’authentification via `/auth/login`.

- **Checklist pour Auth :**  
  - [ ] Définir les schémas de requête et de réponse (`LoginRequest`, `LoginResponse`, `RefreshResponse`).
  - [ ] Implémenter la logique de vérification via Firebase Admin.
  - [ ] Créer des fonctions dans `auth_service.py` pour gérer la logique métier.
  - [ ] Tester avec des cas unitaires et d’intégration.
  - [ ] Documenter l’endpoint dans la documentation OpenAPI.

---

### B. Endpoints de Gestion des Utilisateurs  
- **Endpoints à implémenter :**  
  - **GET `/users`**  
    - Renvoyer une liste paginée des utilisateurs.
  - **POST `/users`**  
    - Créer un nouvel utilisateur (cas d’utilisation du back-office).
  - **GET `/users/{userId}`**  
    - Récupérer les détails d’un utilisateur spécifique.
  - **PATCH `/users/{userId}`**  
    - Mettre à jour partiellement les informations d’un utilisateur.
  - **DELETE `/users/{userId}`**  
    - Supprimer un utilisateur.

- **Checklist pour Users :**  
  - [ ] Définir les schémas (`User`, `UserListResponse`, `UserCreateRequest`, `UserUpdateRequest`).
  - [ ] Implémenter la logique CRUD dans `user_service.py`.
  - [ ] Gérer la vérification du JWT et des permissions via middleware ou dépendances.
  - [ ] Tester les endpoints avec des scénarios de création, lecture, mise à jour et suppression.
  - [ ] Ajouter des validations et des vérifications de sécurité.

---

### C. Endpoints de Gestion des Rôles et Permissions  
- **Endpoints à implémenter :**  
  - **Pour les rôles :**
    - **GET `/roles`**  
      - Renvoyer la liste des rôles.
    - **POST `/roles`**  
      - Créer un nouveau rôle.
    - **PATCH `/roles/{roleId}`**  
      - Mettre à jour un rôle.
    - **DELETE `/roles/{roleId}`**  
      - Supprimer un rôle.
  - **Pour les permissions :**
    - **GET `/permissions`**  
      - Renvoyer la liste des permissions.
    - **POST `/permissions`**  
      - Créer une nouvelle permission.
    - **PATCH `/permissions/{permissionId}`**  
      - Mettre à jour une permission.
    - **DELETE `/permissions/{permissionId}`**  
      - Supprimer une permission.

- **Checklist pour Roles/Permissions :**  
  - [ ] Définir les schémas (`Role`, `RoleCreateRequest`, `RoleUpdateRequest`, `Permission`, `PermissionCreateRequest`, `PermissionUpdateRequest`).
  - [ ] Implémenter la logique dans les services dédiés ou dans un module de gestion d’autorisation.
  - [ ] Mettre en place des vérifications de permissions lors de l’accès aux endpoints sensibles.
  - [ ] Tester avec des scénarios d’administration (création, modification, suppression).

---

### D. Sécurité et Gestion du JWT  
- **Mécanismes à implémenter :**  
  - Middleware ou dépendance FastAPI pour la vérification du JWT.
  - Validation des permissions et des rôles dans les endpoints protégés.
  - Gestion des refresh tokens.

- **Checklist pour Sécurité :**  
  - [ ] Implémenter et tester la fonction de vérification du JWT dans `security.py`.
  - [ ] Intégrer la vérification dans chaque endpoint protégé.
  - [ ] Documenter les exigences de sécurité dans la doc OpenAPI.