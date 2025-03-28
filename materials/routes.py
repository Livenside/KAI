from typing import Annotated
from fastapi import Request, APIRouter, UploadFile, Form, Query, Response
from collections import defaultdict as dd
import urllib.parse
from config import server
from models.file import File
from models.material import Material
from models.material_file import MaterialFile

router = APIRouter(tags=["Materials"])


@router.get("/study-materials")
def materials(request: Request,
		clas: Annotated[str | None, Query(alias="class")] = None,
		quarter: Annotated[str | None, Query(alias="quarter")] = None):
	materials = None
	if clas is not None and quarter is not None:
		materials_db = MaterialFile.get_filtered(server.conn, clas, quarter)
		materials = dd(list)
		for material in materials_db:
			materials[material["material"].topic].append(material)

	context = {
		"results": materials,
		"class": clas,
		"quarter": quarter,
	}
	return server.jinja.TemplateResponse(
		request=request,
		name="materials.html",
		context=context
	)


@router.post("/study-materials")
async def create(file: UploadFile,
		title: str = Form(),
		clas: int = Form(),
		quarter: int = Form(),
		topic: str = Form()):
	f = await File.read(file)
	f.upload(server.conn)

	material = Material(
		title=title,
		file_id=f.id,
		link_url=None,
		clas=clas,
		quarter=quarter,
		topic=topic,
	)

	material.create(server.conn)

	return material

@router.get("/study-materials/{id}/download")
async def download(id: int):
	data = MaterialFile.get_file(server.conn, id)
	fname = urllib.parse.quote(data.fname)
	return Response(
		content=data.fdata,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={fname}"}
	)

