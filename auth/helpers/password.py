import bcrypt

def hash(password: str) -> bytes:
	return bcrypt.hashpw(
		password.encode(),
		bcrypt.gensalt()
	)

def check(password: str, hashed: bytes) -> bool:
	return bcrypt.checkpw(password.encode(), hashed)

