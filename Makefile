build-dist:
	pip install --upgrade pip build
	python -m build

build-docker:
	docker build -t noname .

run-local-uvicorn:
	uvicorn noname.main:app --reload
