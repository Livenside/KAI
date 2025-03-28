-- migrate:up
CREATE TABLE study_materials (
	id INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	file_id CHAR(36),
	link_url TEXT,
	class TINYINT NOT NULL,
	quarter TINYINT NOT NULL,

	PRIMARY KEY(id),
	FOREIGN KEY(file_id) REFERENCES files(id)
);

-- migrate:down
DROP TABLE study_materials;

