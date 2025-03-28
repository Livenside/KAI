-- migrate:up
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

-- migrate:down
DROP TABLE users;

