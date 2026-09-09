CREATE TABLE password_reset_token (
 id BIGINT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL, token_hash VARCHAR(128) NOT NULL UNIQUE,
 expires_at TIMESTAMP NOT NULL, used_at TIMESTAMP NULL,
 CONSTRAINT fk_reset_user FOREIGN KEY (user_id) REFERENCES app_users(id)
);
