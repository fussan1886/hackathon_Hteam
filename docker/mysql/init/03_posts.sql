CREATE TABLE posts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    visibility ENUM('public', 'private') NOT NULL DEFAULT 'public',
    created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted_at TIMESTAMP(6) NULL,
    CONSTRAINT fk_posts_user FOREIGN KEY (user_id) REFERENCES users(id),
     CONSTRAINT fk_posts_category FOREIGN KEY (category_id) REFERENCES categories(id),
    INDEX idx_posts_user_created_at (user_id, created_at),
    INDEX idx_posts_created_at (created_at),
    INDEX idx_posts_category_id (category_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;