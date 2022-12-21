import logging
import time
import uuid
from contextvars import ContextVar

from fastapi.routing import APIRoute
from starlette.background import BackgroundTask


request_id_context = ContextVar('request_id')


class TimedRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger('main.view')

    def log_info(self, req_body, res_body, request_duration):
        self._logger.info(
            msg='Request summary',
            extra={
                'request': req_body.decode(),
                'response': res_body.decode(),
                'duration': request_duration,
            }
        )

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        # Request gets here when path exists.
        async def custom_route_handler(request):
            # TODO: Check if request-id is already in the header. If so, then populate it to the context.
            request_id = uuid.uuid4().hex
            request_id_context.set(request_id)
            self._logger.debug('Started request middleware.')
            start_time = time.perf_counter()
            req_body = await request.body()
            response = await original_route_handler(request)
            end_time = time.perf_counter() - start_time
            request_duration = str(format(end_time, '.3f'))
            response.headers['X-REQUEST-DURATION'] = request_duration
            response.headers['X-REQUEST-ID'] = str(request_id_context.get())
            res_body = response.body
            response.background = BackgroundTask(self.log_info, req_body, res_body, request_duration)
            self._logger.debug('Finished request middleware.')
            return response

        return custom_route_handler
