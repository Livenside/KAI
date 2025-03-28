from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from config import server
import pymysql

import materials.routes
import auth.routes
import tests.routes
import sends.routes
import admin.routes


load_dotenv(".env")

conn = pymysql.connect(
	host=os.getenv("DATABASE_HOST"),
	user=os.getenv("DATABASE_USER"),
	password=os.getenv("DATABASE_PASSWORD"),
	database=os.getenv("DATABASE_DATABASE"),
	autocommit=True,
)

server.conn = conn

server.jinja = Jinja2Templates(directory="templates/")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index(request: Request, name: str | None = None):
	context = {
		"name": name or "Default"
	}
	return server.jinja.TemplateResponse(
		request=request,
		name="index.html",
		context=context)


app.include_router(materials.routes.router)
app.include_router(auth.routes.router)
app.include_router(tests.routes.router)
app.include_router(sends.routes.router)
app.include_router(admin.routes.router)

