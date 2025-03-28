from typing import Annotated
from fastapi import APIRouter, Form, Request, Cookie
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from config import server
from auth.helpers import jwt
from auth.helpers import password as pwd_helper
from models.user import User


router = APIRouter(tags=["Auth"])


def you_shall_not_pass():
	response = RedirectResponse("/login", status_code=303)
	response.delete_cookie(key="token")
	return response


def you_shall_pass(email: str):
	token = jwt.issue(email)
	response = RedirectResponse("/account", status_code=303)
	response.set_cookie(key="token", value=token, expires=jwt.TTL)
	return response


@router.get("/account")
def account(request: Request, token: Annotated[str | None, Cookie()] = None):
	if token is None:
		return you_shall_not_pass()
	valid = jwt.validate(token)
	if not valid:
		return you_shall_not_pass()
	email = valid['sub']
	if not email:
		return you_shall_not_pass()
	user = User.get_by_email(server.conn, email)
	if not user:
		return you_shall_not_pass()
	user = user.__dict__
	return server.jinja.TemplateResponse(
		request=request,
		name="account.html",
		context=user
	)


@router.get("/login")
def login_page(request: Request, error: str | None = None):
	context = {}
	if error == 'wrongpassword':
		context['error'] = 'Неверный пароль'
	if error == 'testnoaccount':
		context['error'] = 'Войдите, чтобы решать тесты'
	return server.jinja.TemplateResponse(
		request=request,
		name="login.html",
		context=context
	)


@router.get("/register")
def register_page(request: Request, error: str | None = None):
	context = {}
	if error == 'emailtaken':
		context['error'] = 'Email уже занят'
	return server.jinja.TemplateResponse(
		request=request,
		name="register.html",
		context=context
	)


@router.post("/login")
def login(request: Request,
		email: EmailStr = Form(),
		password: str = Form()):
	user = User.get_by_email(server.conn, email)
	if not pwd_helper.check(password, user.password_hash):
		return RedirectResponse("/login?error=wrongpassword", status_code=303)
	return you_shall_pass(email)


@router.post("/register")
def register(request: Request,
		email: EmailStr = Form(),
		password: str = Form(),
		first_name: str = Form(),
		last_name: str = Form(),
		clas: int = Form(alias="class")):
	if User.get_by_email(server.conn, email):
		return RedirectResponse("/register?error=emailtaken", status_code=303)

	password_hash = pwd_helper.hash(password)

	user = User(
		email=email,
		password_hash=password_hash,
		first_name=first_name,
		last_name=last_name,
		clas=clas
	)
	user.create(server.conn)

	return you_shall_pass(user.email)


@router.get("/logout")
def logout():
	return you_shall_not_pass()
