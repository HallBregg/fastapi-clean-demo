FROM python:3.11-slim-bullseye as base

LABEL maintainer="hallbregg0@gmail.com"

RUN apt-get update &&\
    apt-get upgrade &&\
    apt-get install -y libcap2-bin inetutils-ping

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

RUN pip install -r requirements.dev.txt
COPY ./src/ .
COPY ./tests .
CMD ["python", "-c", "from noname import __version__; print(f'version in dev: {__version__}')"]

FROM base-deps as production-build

RUN pip install -r requirements.txt .
COPY ./src/ .
RUN pip install .

FROM base as production

COPY --from=production-build /opt/noname/venv /opt/noname/venv
CMD ["python", "-c", "from noname import __version__; print(f'version in prod: {__version__}')"]
