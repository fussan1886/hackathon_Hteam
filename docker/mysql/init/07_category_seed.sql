# テストデータ用
INSERT INTO categories (category_name)
VALUES ('コーヒー豆')
ON DUPLICATE KEY UPDATE category_name = VALUES(category_name);
