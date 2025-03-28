-- migrate:up
ALTER TABLE users
	ADD COLUMN email VARCHAR(255),
	ADD COLUMN password_hash BINARY(60),
	ADD COLUMN class TINYINT;

-- migrate:down
ALTER TABLE users
	DROP COLUMN email,
	DROP COLUMN password_hash,
	DROP COLUMN class;

