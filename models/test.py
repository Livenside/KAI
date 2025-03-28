from .model import Model
from pymysql import Connection

"""
CREATE TABLE tests (
	id        INT     NOT NULL AUTO_INCREMENT,
	name      TEXT    NOT NULL,
	class     TINYINT NOT NULL,
	quarter   TINYINT NOT NULL,
	topic     TEXT    NOT NULL,
	test_data JSON    NOT NULL,

	PRIMARY KEY(id)
);
"""

class Test(Model):
	id: int
	name: str
	clas: int
	quarter: int
	topic: str
	test_data: str | dict

	def __init__(
		self,
		id: int | None = None,
		name: str | None = None,
		clas: int | None = None,
		quarter: int | None = None,
		topic: str | None = None,
		test_data: str | dict | None = None
	):
		self.id = id
		self.name = name
		self.clas = clas
		self.quarter = quarter
		self.topic = topic
		self.test_data = test_data

	@staticmethod
	def get_filtered(conn: Connection, clas: int, quarter: int):
		sql = """
		SELECT id, name, class, quarter, topic
		FROM tests
		WHERE class = %s AND quarter = %s;
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (clas, quarter))
			return [Test(*x) for x in cur.fetchall()]
		
	@staticmethod
	def get_not_filtered(conn: Connection):
		sql = """
		SELECT id, name, class, quarter, topic
		FROM tests
		"""
		with conn.cursor() as cur:
			cur.execute(sql)
			return [Test(*x) for x in cur.fetchall()]

	@staticmethod
	def get_one(conn: Connection, id: int):
		sql = """
		SELECT id, name, class, quarter, topic, test_data
		FROM tests
		WHERE id = %s
		LIMIT 1;
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (id, ))
			return Test(*cur.fetchone())

	def create(self, conn: Connection):
		sql = """
		INSERT INTO tests
			(name, class, quarter, topic, test_data)
		VALUES
			(%s, %s, %s, %s, %s);
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (
				self.name,
				self.clas,
				self.quarter,
				self.topic,
				self.test_data
			))
			self.id = cur.lastrowid
			return self

