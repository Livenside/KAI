from pydantic import Field
from pymysql import Connection
from .model import Model

"""
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash BINARY(60) NOT NULL,
	class TINYINT NOT NULL,

	PRIMARY KEY(id),
	INDEX ix_users_email (email)
);
"""

class User(Model):
	id: int
	first_name: str
	last_name: str
	email: str
	password_hash: bytes
	clas: int = Field(alias="class")

	def __init__(
		self,
		id=None,
		first_name=None,
		last_name=None,
		email=None,
		password_hash=None,
		clas=None
	):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password_hash = password_hash
		self.clas = clas

	@staticmethod
	def get_all(conn: Connection):
		sql = """
		SELECT id, first_name, last_name, email, password_hash, class
		FROM users
		"""
		with conn.cursor() as cur:
			cur.execute(sql)
			return [User(*x) for x in cur.fetchall()]

	@staticmethod
	def get_by_email(conn: Connection, email):
		sql = """
		SELECT id, first_name, last_name, email, password_hash, class
		FROM users
		WHERE email = %s
		LIMIT 1
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (email,))
			if res := cur.fetchone():
				return User(*res)
			return None

	def create(self, conn: Connection):
		sql = """
		INSERT INTO users
			(first_name, last_name, email, password_hash, class)
		VALUES
			(%s, %s, %s, %s, %s)
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (
				self.first_name,
				self.last_name,
				self.email,
				self.password_hash,
				self.clas))
			self.id = cur.fetchone()
			return self.id

