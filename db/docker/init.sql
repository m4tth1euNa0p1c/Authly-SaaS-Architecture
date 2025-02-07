-- =====================================================
-- 1. Création du Schéma
-- =====================================================
CREATE SCHEMA IF NOT EXISTS authly;
SET search_path TO authly;

-- =====================================================
-- 2. Table : roles
-- =====================================================
CREATE TABLE IF NOT EXISTS roles (
    id           BIGSERIAL PRIMARY KEY,
    name         VARCHAR(50) NOT NULL UNIQUE, 
    description  TEXT DEFAULT '',
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- 3. Table : permissions
-- =====================================================
CREATE TABLE IF NOT EXISTS permissions (
    id           BIGSERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE, 
    description  TEXT DEFAULT '',
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- 4. Table de liaison : role_permissions
-- =====================================================
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id       BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    granted_at    TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (role_id, permission_id),
    CONSTRAINT fk_rp_role FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
    CONSTRAINT fk_rp_permission FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE
);

-- =====================================================
-- 5. Table : users
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id                BIGSERIAL        PRIMARY KEY,
    email             VARCHAR(150)     NOT NULL UNIQUE,
    hashed_password   VARCHAR(255)     NOT NULL,
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    email_verified    BOOLEAN          DEFAULT FALSE,
    is_active         BOOLEAN          NOT NULL DEFAULT TRUE,
    last_login        TIMESTAMPTZ,
    created_at        TIMESTAMPTZ      DEFAULT NOW(),
    updated_at        TIMESTAMPTZ      DEFAULT NOW()
);


-- =====================================================
-- 6. Table de liaison : user_roles
-- =====================================================
CREATE TABLE IF NOT EXISTS user_roles (
    user_id     BIGINT NOT NULL,
    role_id     BIGINT NOT NULL,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_ur_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_ur_role FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE
);

-- =====================================================
-- 7. Table : refresh_tokens
-- =====================================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL,
    refresh_token   VARCHAR(500) NOT NULL UNIQUE,
    issued_at       TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL,
    revoked         BOOLEAN DEFAULT FALSE,
    revoked_at      TIMESTAMPTZ,
    CONSTRAINT fk_rt_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- =====================================================
-- 8. Table : oauth_providers
-- =====================================================
CREATE TABLE IF NOT EXISTS oauth_providers (
    id             BIGSERIAL PRIMARY KEY,
    name           VARCHAR(50) NOT NULL UNIQUE, 
    client_id      VARCHAR(200) NOT NULL, 
    client_secret  VARCHAR(200) NOT NULL,
    created_at     TIMESTAMPTZ DEFAULT NOW(),
    updated_at     TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- 9. Table : user_oauth_sessions
-- =====================================================
CREATE TABLE IF NOT EXISTS user_oauth_sessions (
    id               BIGSERIAL PRIMARY KEY,
    user_id          BIGINT NOT NULL,
    provider_id      BIGINT NOT NULL,
    provider_uid     VARCHAR(200) NOT NULL,  -- Identifiant unique renvoyé par le provider
    access_token     VARCHAR(500),
    refresh_token    VARCHAR(500),
    token_expires_at TIMESTAMPTZ,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_uos_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_uos_provider FOREIGN KEY (provider_id) REFERENCES oauth_providers (id) ON DELETE CASCADE
);

-- =====================================================
-- 10. Triggers pour mise à jour automatique de updated_at sur users
-- =====================================================
CREATE OR REPLACE FUNCTION update_timestamp_users()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_users_updated ON users;
CREATE TRIGGER tr_users_updated
BEFORE UPDATE ON users
FOR EACH ROW 
EXECUTE FUNCTION update_timestamp_users();
