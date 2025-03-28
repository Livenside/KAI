-- migrate:up
ALTER TABLE users
	MODIFY COLUMN email VARCHAR(255) NOT NULL UNIQUE,
	MODIFY COLUMN password_hash BINARY(60) NOT NULL,
	MODIFY COLUMN class TINYINT NOT NULL,
	ADD INDEX ix_users_email (email);

-- migrate:down
ALTER TABLE users
	MODIFY COLUMN email VARCHAR(255),
	MODIFY COLUMN password_hash BINARY(60),
	MODIFY COLUMN class TINYINT,
	DROP INDEX ix_users_email;

