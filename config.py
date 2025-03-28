from pymysql import Connection
from fastapi.templating import Jinja2Templates


class Config:
    jinja: Jinja2Templates
    conn: Connection


server = Config()
