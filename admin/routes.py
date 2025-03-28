from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import RedirectResponse
from config import server
# from models.user import User
from models.user_test_result import UserTestResult
from models.work import Work
from models.file import File
from auth.helpers import jwt
from models.test import Test
from collections import defaultdict

from collections import defaultdict as dd


router = APIRouter(tags=["Admin"])


@router.get("/admin/login")
async def login_page(request: Request, error: str | None = None):
	context = {}
	if error == 'wrongpassword':
		context['error'] = 'Неверный пароль'
	return server.jinja.TemplateResponse(
		request=request,
		name="admin_login.html",
		context=context
	)


@router.post("/admin/login")
async def login(request: Request,
		email: str = Form(),
		password: str = Form()):
	if email != "admin" or password != "12345678":
		return RedirectResponse("/admin/login?error=wrongpassword", status_code=303)
	token = jwt.issue(email)
	response = RedirectResponse("/admin", status_code=303)
	response.set_cookie(key="token", value=token, expires=jwt.TTL)
	return response


@router.get("/admin")
async def admin(request: Request, token: str | None = Cookie()):
	if (validate := jwt.validate(token)) and validate['sub'] != "admin":
		return RedirectResponse("/", status_code=303)

	test_results = UserTestResult.get_all(server.conn)
	test_results_alt = UserTestResult.get_students_test(server.conn)
	tests = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
	tests_db = Test.get_not_filtered(server.conn)
	for test in tests_db:
		if test.clas is not None and 6 <= test.clas <= 9:
			if test.quarter is not None and 1 <= test.quarter <= 4:
				tests[test.clas][test.quarter][test.topic][test.name].append(test)

		tests[test.clas][test.quarter][test.topic][test.name].append(test)
	
	works = Work.get_all(server.conn)
	return server.jinja.TemplateResponse(
		request=request,
		name="admin.html",
		context={"results": test_results, "results_alt": test_results_alt, "tests": tests, "works": works, "file_name": lambda file_id: File.get_name_by_id(file_id, server.conn)}
	)
