FROM python:3.11-slim-bullseye as base
LABEL maintainer="hallbregg0@gmail.com"

RUN apt-get update &&\
    apt-get upgrade &&\
    apt-get install -y libcap2-bin inetutils-ping

WORKDIR /opt/noname
RUN useradd --create-home noname
RUN chown -R noname:root /opt/noname

USER noname
CMD ["/sbin/getpcaps", "1"]

FROM base as build

ENV VIRTUAL_ENV=/opt/noname/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

COPY ./requirements.dev.txt .
COPY ./requirements.txt .
COPY ./pyproject.toml .

RUN pip install -r requirements.dev.txt

COPY ./src/ .

CMD ["python", "-c", "from noname import __version__; print(f'version: {__version__}')"]
