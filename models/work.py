from pymysql import Connection
from models.model import Model
from datetime import datetime
from models.file import File
from config import server
import uuid

"""
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
"""

class Work(Model):
    id: int
    file_id: uuid.UUID
    user_id: int
    score: int
    max_score: int
    sent_at: int
    score_detail: str
    sent_detail: str

    def __init__(
        self,
        id: int | None = None,
        file_id: uuid.UUID | None = None,
        user_id: int | None = None,
        score: int | None = None,
        max_score: int | None = None,
        sent_at: int | None = None,
        score_detail: str | None = None,
        sent_detail: str | None = None
    ):
        self.id = id
        self.file_id = file_id
        self.user_id = user_id
        self.score = score
        self.max_score = max_score
        self.sent_at = sent_at
        if sent_at is not None:
            self.sent = datetime.fromtimestamp(sent_at).strftime('%d.%m.%Y %H:%M:%S')
        else:
            self.sent = "No timestamp provided"

        self.user_name = get_user_name(self.user_id, server.conn)
        self.user_class = get_user_class(self.user_id, server.conn)
        self.score_detail = score_detail
        self.sent_detail = sent_detail

    def send(self, conn: Connection):
        sql = """
        INSERT INTO students_works
            (file_id, user_id, sent_at, sent_detail, score, max_score)
        VALUES
            (%s, %s, unix_timestamp(), %s, 0, 0)
        """
        with conn.cursor() as cur:
            cur.execute(sql, (
                self.file_id,
                self.user_id,
                self.sent_detail
            ))
            self.id = cur.lastrowid
            conn.commit()
            return self

    @classmethod
    def get_all(cls, conn: Connection):
        sql = "SELECT * FROM students_works"
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            works = []
            for row in rows:
                # Пример преобразования: row[1] соответствует file_id
                row = list(row)
                row[1] = uuid.UUID(row[1])
                works.append(cls(*row))
            return works

    @staticmethod
    def get_file(conn: Connection, file_id: int):
        sql = """
        SELECT F.id, F.fname, F.fsize, F.fdata
        FROM
            students_works AS S
            LEFT JOIN files AS F ON S.file_id = F.id
        WHERE S.id = %s
        LIMIT 1
        """

        with conn.cursor() as cur:
            cur.execute(sql, (file_id,))
            return File(cur.fetchone())
        
def get_user_name(user_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    return row[0] + " " + row[1] if row else ""

def get_user_class(user_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT class FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else ""