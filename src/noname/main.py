import asyncio
import logging
import random
import socket
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI


class LoggingConfig:

    @classmethod
    def init_dependencies(cls):
        logging.getLogger('uvicorn.access').setLevel(logging.INFO)
        logging.getLogger('uvicorn.error').setLevel(logging.INFO)
        logging.getLogger('gunicorn.access').setLevel(logging.DEBUG)
        logging.getLogger('gunicorn.error').setLevel(logging.DEBUG)

    @classmethod
    def init_application(cls):
        logger = logging.getLogger('main')
        logger_handler = logging.StreamHandler()
        logger_formatter = logging.Formatter('%(asctime)s %(process)d %(name)s %(message)s')
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_handler)
        logger.propagate = False

    @classmethod
    def init(cls):
        logging.basicConfig(level=logging.DEBUG)
        cls.init_dependencies()
        cls.init_application()


LoggingConfig.init()
app = FastAPI()


class HostnameService:
    @staticmethod
    async def get_hostname():
        return socket.gethostname()


class WebContextLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg, kwargs = super().process(msg, kwargs)
        return f'{request_id_context.get()} {msg}', kwargs


http_logger = WebContextLoggerAdapter(logging.getLogger('main.http'), {})
request_id_context = ContextVar('request_id')


@app.middleware('http')
async def request_context_middleware(request, call_next):
    # We could log from BackgroundTask to make it non blockable.
    request_id = uuid.uuid4().hex
    request_id_context.set(request_id)
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time() - start_time
    response.headers['X-REQUEST-DURATION'] = str(format(end_time, '.3f'))
    response.headers['X-REQUEST-ID'] = str(request_id_context.get())
    return response


@app.get('/')
async def home():
    http_logger.debug('DEBUG. Called home view.')
    http_logger.info('INFO. Called home view.')
    http_logger.warning('WARNING. Called home view.')
    http_logger.error('ERROR. Called home view.')
    http_logger.critical('CRITICAL. Called home view.')
    await asyncio.sleep(random.randint(1, 3))
    return {'host': await HostnameService.get_hostname()}
