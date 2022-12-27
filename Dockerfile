FROM python:3.11-slim-bullseye as base

LABEL maintainer="hallbregg0@gmail.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update &&\
    apt-get upgrade &&\
    apt-get install --no-install-recommends -y htop &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*
#    libcap2-bin inetutils-ping

WORKDIR /opt/noname

# We can also disable home directory and shell access to the user:
#RUN addgroup --gid 1001 --system noname && \
#    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group noname

RUN useradd --create-home noname &&\
    chown -R noname:root /opt/noname
USER noname

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV VIRTUAL_ENV=/opt/noname/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["/sbin/getpcaps", "1"]

FROM base as base-deps

RUN python -m venv $VIRTUAL_ENV

COPY ./requirements.dev.txt .
COPY ./requirements.txt .
COPY ./pyproject.toml .

FROM base-deps as development

ENV PYTHONASYNCIODEBUG 1
RUN pip install --no-cache-dir -r requirements.dev.txt
COPY ./src/ .
COPY ./tests .
CMD ["python", "-c", "from noname import __version__; print(f'version in dev: {__version__}')"]

FROM base-deps as production-build

RUN pip install --no-cache-dir -r requirements.txt .
COPY ./src/ .
RUN pip install .

FROM base as production

EXPOSE 80
COPY --from=production-build /opt/noname/venv /opt/noname/venv
#CMD ["python", "-c", "from noname import __version__; print(f'version in prod: {__version__}')"]
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "-k", "uvicorn.workers.UvicornWorker", "--workers", "3", "-b", "0.0.0.0:80", "noname.main:app"]
