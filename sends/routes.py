from fastapi import APIRouter, Request, UploadFile, Form, Cookie, Response
from fastapi.responses import RedirectResponse
from models.file import File
from models.work import Work
from models.user import User
from models.material import Material
from models.work import Work
from models.test import Test
from config import server
from auth.helpers import jwt

from tests.parser import parser

import json
import urllib.parse

router = APIRouter(tags=["Student Works"])

@router.post("/send")
async def send(
	request: Request,
	file: UploadFile = File(),
	comment: str = Form(),
	token: str = Cookie()
):
	f = await File.read(file)
	f.upload(server.conn)

	if (validate := jwt.validate(token)) and (email := validate['sub']):
		user = User.get_by_email(server.conn, email).__dict__

		work = Work(
			file_id=f.id,
			user_id=user["id"],
			sent_detail=comment
		)
		work.send(server.conn)

	return server.jinja.TemplateResponse(
		request=request,
		name="sent.html",
	)

@router.get("/work")
def list_works(request: Request):
    works = Work.get_all(server.conn)
    context = {"works": works}
    return server.jinja.TemplateResponse("admin.html", {"request": request, **context})

@router.get("/admin/works/{id}/download")
async def download(id: int):
	data = Work.get_file(server.conn, id)
	fname = urllib.parse.quote(data.fname)
	return Response(
		content=data.fdata,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={fname}"}
	)

@router.post("/admin/sendMaterial")
async def sendMaterial(
	file: UploadFile = File(),
	topicc: str = Form(),
	titlee: str = Form(),
	classs: int = Form(),
	quart: int = Form()
):
	f = await File.read(file)
	f.upload(server.conn)

	material = Material(
			file_id=f.id,
			topic=topicc,
			title=titlee,
			clas=classs,
			quarter=quart
		)
	material.create(server.conn)
	return RedirectResponse(url="/admin", status_code=303)

@router.post("/admin/sendTest")
async def sendTest(
	file: UploadFile = File(),
	topicc: str = Form(),
	titlee: str = Form(),
	classs: int = Form(),
	quart: int = Form(),

):
	content = await file.read()
	text = content.decode('utf-8')
	
	test_dat = parser.parse(text)

	test = Test(
			topic=topicc,
			name=titlee,
			clas=classs,
			quarter=quart,
			test_data=test_dat
		)
	test.test_data = json.dumps(test_dat, ensure_ascii=False)
	test.create(server.conn)
	return RedirectResponse(url="/admin", status_code=303)