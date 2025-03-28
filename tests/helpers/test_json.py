import json
from pydantic import BaseModel, Field, TypeAdapter


class TestHeaders(BaseModel):
	number: str | int
	topic: str
	clas: str | int = Field(alias="class")

class Question(BaseModel):
	wording: str
	options: list[str]
	right: int

class TestData(BaseModel):
	headers: TestHeaders
	questions: list[Question]


test_ta = TypeAdapter(TestData)


def get_data(json_text: str) -> TestData:
	return test_ta.validate_python(json.loads(json_text))


def is_valid_test(json_text: str) -> bool:
	try:
		get_data(json_text)
	except Exception:
		return False
	else:
		return True


if __name__ == "__main__":
	with open('../parser/test1.json', 'r') as f:
		json_text = f.read()
		print(is_valid_test(json_text))


