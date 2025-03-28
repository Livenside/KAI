-- migrate:up
CREATE TABLE files (
	id CHAR(36) NOT NULL,
	fname VARCHAR(255) NOT NULL,
	fsize INT NOT NULL,
	fdata LONGBLOB NOT NULL,

	PRIMARY KEY(id)
);

-- migrate:down
DROP TABLE files;

