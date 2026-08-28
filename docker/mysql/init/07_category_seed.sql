# テストデータ用
SET NAMES utf8mb4;
INSERT INTO categories (category_name)
VALUES ('コーヒー豆'), ('抽出器具'), ('コーヒーショップ'), ('淹れ方'), ('その他')
ON DUPLICATE KEY UPDATE category_name = VALUES(category_name);
