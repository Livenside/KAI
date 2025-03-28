import re
import json
import io


def parse_headers(header: str) -> dict:
	number = header[:header.find(' ')]
	topic = re.search(r'«.+»', header).group()[1:-1]
	class_number = re.search(r'\d+ класс', header).group().split()[0]

	return {
		"number": number,
		"topic": topic,
		"class": class_number
	}


def parse_tokens(tokens: list[str]) -> list[dict[str]]:
	questions = []
	question = None
	for token in tokens:
		if not token:
			continue
		if token[:6] == 'Вопрос':
			if question is not None:
				questions.append(question)
			question = {}
			question["wording"] = token[10:].strip()
			question["options"] = []
		else:
			if token[0] == "*":
				question["right"] = len(question["options"]) + 1
			question["options"].append(token[token.find(")")+1:].strip())
	else:
		questions.append(question)

	return questions


def parse(data: io.TextIOBase | str):
	if isinstance(data, str):
		data = io.StringIO(data)
	headers = parse_headers(data.readline())
	tokens = [
		x.strip()
		for x in re.split(r'   |\n|\xa0\xa0\xa0', data.read())
		if x
	]
	return {
		"headers": headers,
		"questions": parse_tokens(tokens)
	}


if __name__ == "__main__":
	with open('./cases/test2.txt') as f:
		res = parse(f)
	with open('test2.json', 'w', encoding="utf-8") as f:
		f.write(json.dumps(res, ensure_ascii=False))

