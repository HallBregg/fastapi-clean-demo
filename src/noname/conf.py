import logging


class RequestIdInjectorFilter(logging.Filter):
    def __init__(self, name='request_id_injector'):
        from noname.utils import request_id_context
        super().__init__(name)
        self._request_id_context = request_id_context

    def _logic(self, record):
        try:
            setattr(record, 'request_id', self._request_id_context.get())
        except LookupError:
            # Application has not started yet. CustomFilter is applied on process manager logs.
            record.request_id = None

    def filter(self, record: logging.LogRecord) -> bool:
        self._logic(record)
        return True


class ExtraFormatter(logging.Formatter):
    FORMAT = '%(asctime)s | %(process)d | %(levelname)s | %(name)s | %(message)s | %(extras)s'

    def __init__(self, fmt=None, *args, **kwargs):
        fmt = fmt or self.FORMAT
        super().__init__(fmt, *args, **kwargs)

    """ formatter which let see all extra passed to log record """
    def format(self, record):
        # inspired by https://stackoverflow.com/questions/39965807/python-log-formatter-that-shows-all-kwargs-in-extra/39974319  # noqa
        dummy = logging.LogRecord(None, None, None, None, None, None, None)
        extras = {}
        for k, v in record.__dict__.items():
            if k not in dummy.__dict__:
                extras[k] = v
        record.extras = extras
        return super().format(record)


level = logging.DEBUG

# Configure root logging. Catch all loggers from dependencies.
# https://github.com/encode/uvicorn/issues/680#issuecomment-675495385
for log_name in logging.root.manager.loggerDict.keys():
    if log_name in []:  # list of loggers
        logging.getLogger(log_name).handlers = [logging.NullHandler()]
        logging.getLogger(log_name).propagate = False
    else:
        logging.getLogger(log_name).handlers = []
        logging.getLogger(log_name).propagate = True

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(ExtraFormatter())
logger_handler.addFilter(RequestIdInjectorFilter())
logging.root.handlers = [logger_handler]
logging.root.setLevel(level)


# Configure application logger (root for this app).
logger = logging.getLogger('main')
logger.propagate = False

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(ExtraFormatter())
logger_handler.addFilter(RequestIdInjectorFilter())

logger.handlers = [logger_handler]
logger.setLevel(level)
