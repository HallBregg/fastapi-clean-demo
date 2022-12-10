build-dist:
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
		-v ${PWD}/src/noname:/opt/noname/noname \
		-v ${PWD}/tests:/opt/noname/tests noname.dev \
		bash

run-local-uvicorn:
	uvicorn noname.main:app --reload
