import random
import time
import uuid

from fastapi import FastAPI

from noname.services.hostname import HostnameService
from noname.utils import request_id_context
from noname.conf import *

from fastapi.routing import APIRoute, APIRouter
from starlette.background import BackgroundTask


view_logger = logging.getLogger('main.view')


class TimedRoute(APIRoute):

    def log_info(self, req_body, res_body):
        view_logger.info('Request summary', extra={'request': req_body.decode(), 'response': res_body.decode()})

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        # Request gets here when path exists.
        async def custom_route_handler(request):
            # TODO: Check if request-id is already in the header. If so, then populate it to the context.
            request_id = uuid.uuid4().hex
            request_id_context.set(request_id)
            start_time = time.perf_counter()
            req_body = await request.body()
            response = await original_route_handler(request)
            end_time = time.perf_counter() - start_time
            response.headers['X-REQUEST-DURATION'] = str(format(end_time, '.3f'))
            response.headers['X-REQUEST-ID'] = str(request_id_context.get())
            res_body = response.body
            response.background = BackgroundTask(self.log_info, req_body, res_body)
            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=TimedRoute)


@router.get('/')
async def home():
    view_logger.info('Called home view.')
    if random.choice([True, False]):
        try:
            raise Exception('Test exception')
        except Exception as e:
            view_logger.exception(e)
            return {'error': str(e)}
    return {'host': await HostnameService().get_hostname()}


@router.get('/test')
async def test():
    view_logger.debug('Hello World', extra={'hello': 'extra'})
    return {'hello': 'test'}


app.include_router(router)
