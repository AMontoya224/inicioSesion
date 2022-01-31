

USE inicio_sesion;

SELECT *
FROM users;

INSERT INTO users(first_name, last_name, email, password, gender, created_at, update_at) 
VALUES('Ana', 'Lopez', 'ana@gmail.com', 'pass123', 'female', NOW(), NOW());

DELETE FROM users WHERE id>0;

ALTER TABLE users CHANGE password password VARCHAR(255);