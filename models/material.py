import uuid
from pymysql import Connection
from pydantic import Field
from .model import Model

"""
CREATE TABLE study_materials (
	id INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	file_id CHAR(36),
	link_url TEXT,
	class TINYINT NOT NULL,
	quarter TINYINT NOT NULL,
	topic VARCHAR(255) NOT NULL,

	PRIMARY KEY(id),
	FOREIGN KEY(file_id) REFERENCES files(id)
);
"""

class Material(Model):
	id: int
	title: str
	file_id: uuid.UUID | None
	link_url: str | None
	clas: int = Field(alias="class")
	quarter: int
	topic: str

	def __init__(
		self,
		id: int | None = None,
		title: str | None = None,
		file_id: uuid.UUID | None = None,
		link_url: str | None = None,
		clas: int | None = None,
		quarter: int | None = None,
		topic: str | None = None
	):
		self.id = id
		self.title = title
		self.file_id = file_id
		self.link_url = link_url
		self.clas = clas
		self.quarter = quarter
		self.topic = topic

	def __repr__(self):
		return f"[{self.title}]"

	def create(self, conn: Connection):
		sql = """
		INSERT INTO study_materials
			(title, file_id, link_url, class, quarter, topic)
		VALUES
			(%s, %s, %s, %s, %s, %s);
		"""
		with conn.cursor() as cur:
			cur.execute(sql, (
				self.title,
				self.file_id,
				self.link_url,
				self.clas,
				self.quarter,
				self.topic
			))
			self.id = cur.lastrowid
			return self
		conn.commit()

