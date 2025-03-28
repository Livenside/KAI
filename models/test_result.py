from models.model import Model
from pymysql import Connection

from datetime import datetime


"""
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
"""

class TestResult(Model):
	id: int
	test_id: int
	user_id: int
	score: int
	max_score: int
	sent_at: int

	def __init__(
		self,
		id: int | None = None,
		test_id: int | None = None,
		user_id: int | None = None,
		score: int | None = None,
		max_score: int | None = None,
		sent_at: int | None = None,
	):
		self.id = id
		self.test_id = test_id
		self.user_id = user_id
		self.score = score
		self.max_score = max_score
		self.sent_at = sent_at
		if sent_at is not None:
			self.sent = datetime.fromtimestamp(sent_at).strftime('%d.%m.%Y %H:%M:%S')
		else:
			self.sent = "No timestamp provided"

	def save(self, conn: Connection):
		sql = """
		INSERT INTO test_results
			(test_id, user_id, score, max_score, sent_at)
		VALUES
			(%s, %s, %s, %s, unix_timestamp());
		"""

		with conn.cursor() as cur:
			cur.execute(sql, (
				self.test_id,
				self.user_id,
				self.score,
				self.max_score
			))
			self.id = cur.lastrowid
			return self

