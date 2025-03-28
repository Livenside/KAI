from fastapi import Request, APIRouter, Form, Query, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from typing import Annotated
from collections import defaultdict as dd
from config import server
from models.test import Test
from models.user import User
from models.test_result import TestResult
from tests.helpers import test_json as json_helper
from auth.helpers import jwt

router = APIRouter(tags=["Tests"])


@router.get("/tests")
def tests(request: Request,
		clas: Annotated[str | None, Query(alias="class")] = None,
		quarter: Annotated[str | None, Query(alias="quarter")] = None):
	tests = None
	if clas is not None and quarter is not None:
		tests_db = Test.get_filtered(server.conn, clas, quarter)
		tests = dd(list)
		for test in tests_db:
			tests[test.topic].append(test)

	context = {
		"results": tests,
		"class": clas,
		"quarter": quarter,
	}
	return server.jinja.TemplateResponse(
		request=request,
		name="tests.html",
		context=context
	)


@router.post("/tests")
def create(
	name: str = Form(),
	clas: int = Form(),
	quarter: int = Form(),
	topic: str = Form(),
	test_data: str = Form()
):
	if not json_helper.is_valid_test(test_data):
		return HTTPException(status_code=422, detail="invalid test json")

	test = Test(
		name=name,
		clas=clas,
		quarter=quarter,
		topic=topic,
		test_data=test_data
	)

	return test.create(server.conn)


@router.get("/tests/{id}")
def get_one(request: Request, id: int, token: Annotated[str | None, Cookie()] = None):
	if token is None:
		return RedirectResponse("/login?error=testnoaccount", status_code=303)
	context = {
		"test": json_helper.get_data(Test.get_one(server.conn, id).test_data)
	}

	return server.jinja.TemplateResponse(
		request=request,
		name="test.html",
		context=context
	)


@router.post("/tests/{id}")
async def check(request: Request, id: int, token: str | None = Cookie()):
	test = json_helper.get_data(Test.get_one(server.conn, id).test_data)
	form = await request.form()

	answers = [int(form[x]) for x in form]
	rights = [x.right for x in test.questions]

	right_count = sum(1 if a == r else 0 for a, r in zip(answers, rights))
	max_count = len(test.questions)

	if (validate := jwt.validate(token)) and (email := validate['sub']):
		user = User.get_by_email(server.conn, email).__dict__

		test_result = TestResult(
			test_id=id,
			user_id=user["id"],
			score=right_count,
			max_score=max_count
		)
		test_result.save(server.conn)

	context = {
		"test": test,
		"right": right_count,
		"max": max_count,
	}
	return server.jinja.TemplateResponse(
		request=request,
		name="test_results.html",
		context=context
	)
