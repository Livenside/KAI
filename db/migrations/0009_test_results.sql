-- migrate:up
CREATE TABLE test_results (
	id        INT     NOT NULL AUTO_INCREMENT,
	test_id   INT     NOT NULL,
	user_id   INT     NOT NULL,
	score     TINYINT NOT NULL,
	max_score TINYINT NOT NULL,
	sent_at   INT     NOT NULL,

	PRIMARY KEY(id),
	FOREIGN KEY(test_id) REFERENCES tests(id),
	FOREIGN KEY(user_id) REFERENCES users(id)
);

-- migrate:down
DROP TABLE test_results;

