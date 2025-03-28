import jwt
import time
import os


_ALGORITHM = "HS256"
TTL = 60 * 60 * 24 * 30

def issue(email: str):
	return jwt.encode(
		{"sub": email, "exp": int(time.time()) + TTL},
		key=os.getenv("JWT_SECRET"),
		algorithm=_ALGORITHM
	)


def validate(token: str):
	try:
		payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[_ALGORITHM])
	except jwt.exceptions.DecodeError:
		return False
	if time.time() > payload["exp"]:
		return False
	return payload

