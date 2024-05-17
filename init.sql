CREATE DATABASE IF NOT EXISTS sssctf2024_db;

USE sssctf2024_db;

CREATE TABLE IF NOT EXISTS sssctf2024_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO sssctf2024_users (username, password) VALUES ('Scr1w_admin', 'sssctf2024_P@ssvv0rd');
