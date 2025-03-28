import uuid
from pymysql import Connection
from fastapi import UploadFile
from .model import Model

"""
CREATE TABLE files (
	id CHAR(36) NOT NULL,
	fname VARCHAR(255),
	fsize INT,
	fdata LONGBLOB,

	PRIMARY KEY(id)
);
"""

class File(Model):
	id: uuid.UUID
	fname: str
	fsize: int
	fdata: bytes

	def __init__(
		self,
		fetched: tuple | None = None,
		id: uuid.UUID | str | None = None,
		fname: str | None = None,
		fsize: int | None = None,
		fdata: bytes | None = None
	):
		if fetched is not None:
			self.id = fetched[0]
			self.fname = fetched[1]
			self.fsize = fetched[2]
			self.fdata = fetched[3]
			return

		if isinstance(id, str):
			id = uuid.UUID(id)

		self.id = id
		self.fname = fname
		self.fsize = fsize
		self.fdata = fdata

	def __repr__(self):
		return f'[{self.fname}]'

	@staticmethod
	async def read(file: UploadFile):
		self = File()
		self.fname = file.filename
		self.fsize = file.size
		self.fdata = await file.read()
		return self

	def upload(self, conn: Connection):
		sql = """
		INSERT INTO files
			(id, fname, fsize, fdata)
		VALUES
			(%s, %s, %s, %s);
		"""
		uid = uuid.uuid4()
		with conn.cursor() as cur:
			cur.execute(sql, (str(uid), self.fname, self.fsize, self.fdata))
			self.id = uid
			return self

	def get_name_by_id(file_id: int, conn):
		cursor = conn.cursor()
		cursor.execute("SELECT fname FROM files WHERE id = %s", (file_id,))
		row = cursor.fetchone()
		return row[0] if row else ""