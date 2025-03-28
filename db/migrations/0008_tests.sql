-- migrate:up
CREATE TABLE tests (
	id        INT     NOT NULL AUTO_INCREMENT,
	name      TEXT    NOT NULL,
	class     TINYINT NOT NULL,
	quarter   TINYINT NOT NULL,
	topic     TEXT    NOT NULL,
	test_data JSON    NOT NULL,

	PRIMARY KEY(id)
);

-- migrate:down
DROP TABLE tests;

