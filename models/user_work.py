from models.model import Model
from models.work import Work
from models.user import User

from pymysql import Connection


class UserWork(Model):
	work: Work
	user: User

	@staticmethod
	def get_all(conn: Connection):
		sql = """
		SELECT
			TR.id
			, TR.test_id
			, TR.user_id
			, TR.score
			, TR.max_score
			, TR.sent_at
			, U.id
			, U.first_name
			, U.last_name
			, U.email
			, U.password_hash
			, U.class
		FROM students_works TR
			LEFT JOIN users U ON TR.user_id = U.id
		ORDER BY TR.sent_at DESC
		LIMIT 10;
		"""
		with conn.cursor() as cur:
			cur.execute(sql)
			return [
				{
					"test_result": Work(*x[:6]),
					"user": User(*x[6:])
				}
				for x in cur.fetchall()
			]

