from pymysql import Connection
from .model import Model
from .material import Material
from .file import File


class MaterialFile(Model):
	material: Material
	file: File

	@staticmethod
	def get_filtered(conn: Connection, clas: int, quarter: int):
		sql = """
		SELECT S.id, title, file_id, link_url, class, quarter, topic, fsize, fname
		FROM
			study_materials AS S
			LEFT JOIN files AS F ON S.file_id = F.id
		WHERE S.class = %s AND S.quarter = %s
		ORDER BY topic
		"""

		with conn.cursor() as cur:
			cur.execute(sql, (clas, quarter))

			return [{
				"material": Material(*x[:7]),
				"file": File(id=x[2], fsize=x[7], fname=x[8])
			} for x in cur.fetchall()]

	@staticmethod
	def get_file(conn: Connection, material_id: int):
		sql = """
		SELECT F.id, F.fname, F.fsize, F.fdata
		FROM
			study_materials AS S
			LEFT JOIN files AS F ON S.file_id = F.id
		WHERE S.id = %s
		LIMIT 1
		"""

		with conn.cursor() as cur:
			cur.execute(sql, (material_id,))

			return File(cur.fetchone())

