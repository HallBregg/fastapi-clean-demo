import logging
import socket


class HostnameService:
    def __init__(self):
        self._logger = logging.getLogger(f'main.{__name__}')

    async def get_hostname(self):
        hostname = socket.gethostname()
        self._logger.debug(f'Retrieved hostname: {hostname}')
        return hostname
