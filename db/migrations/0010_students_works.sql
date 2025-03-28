-- migrate:up
CREATE TABLE students_works (
	id           INT      NOT NULL AUTO_INCREMENT,
	file_id      CHAR(36) NOT NULL,
	user_id      INT      NOT NULL,
	score        TINYINT  NOT NULL,
	max_score    TINYINT  NOT NULL,
	sent_at      INT      NOT NULL,
	score_detail TEXT,
	sent_detail  TEXT,

	PRIMARY KEY(id),
	FOREIGN KEY(file_id) REFERENCES files(id),
	FOREIGN KEY(user_id) REFERENCES users(id)
);

-- migrate:down
DROP TABLE students_works;

