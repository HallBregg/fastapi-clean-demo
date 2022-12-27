import datetime
import logging


class LinkService:
    def __init__(self):
        self._logger = logging.getLogger(f'main.{__name__}')
        self._logger.debug('LinkService initialized')
        self._mock_storage = []

    def create_link(self, name: str, url: str):

        created_at = datetime.datetime.now()
