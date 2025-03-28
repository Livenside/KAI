from models.model import Model
from models.test_result import TestResult
from models.user import User
from models.test import Test

from pymysql import Connection


class UserTestResult(Model):
	test_result: TestResult
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
			, T.class AS test_class
			, T.quarter AS test_quarter
			, T.topic AS test_topic
			, T.name AS test_name
		FROM test_results AS TR
			LEFT JOIN users AS U ON TR.user_id = U.id
			LEFT JOIN tests AS T ON TR.test_id = T.id
		ORDER BY TR.sent_at DESC
		"""
		with conn.cursor() as cur:
			cur.execute(sql)
			return [
				{
					"test_result": TestResult(*x[:6]),
                    "user": User(*x[6:12]),
                    "test_class": x[12],
					"test_quarter": x[13],
					"test_topic": x[14],
					"test_name": x[15]
				}
				for x in cur.fetchall()
			]

	@staticmethod
	def get_students_test(conn: Connection):
		sql = """
		SELECT
			TR.id,
			TR.test_id,
			TR.user_id,
			TR.score,
			TR.max_score,
			TR.sent_at,
			U.id,
			U.first_name,
			U.last_name,
			U.email,
			U.password_hash,
			U.class
		FROM test_results AS TR  
			LEFT JOIN users AS U ON TR.user_id = U.id
		ORDER BY TR.sent_at DESC;
		"""

		with conn.cursor() as cur:
			cur.execute(sql)
			return [
				{
					"test_result": TestResult(*x[:6]),
					"user": User(*x[6:])
				}
				for x in cur.fetchall()
			]