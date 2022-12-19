local-build-dist:
	pip install --upgrade pip build
	python -m build

docker-build:
	docker build -t noname --file Dockerfile .

docker-build-development:
	docker build -t noname.dev --target development --file Dockerfile .

docker-build-production:
	docker build -t noname.prod --target production --file Dockerfile .

docker-run-development-bash:
	make docker-build-development
	docker run \
		--rm -it \
		-p 8080:8080 \
		-v ${PWD}/src/noname:/opt/noname/noname \
		-v ${PWD}/tests:/opt/noname/tests noname.dev \
		bash

local-run-uvicorn:
	uvicorn noname.main:app --reload --workers 1

local-run-gunicorn:
	gunicorn -k uvicorn.workers.UvicornWorker --reload --workers 1 noname.main:app

local-run-tests:
	pytest -v -s
