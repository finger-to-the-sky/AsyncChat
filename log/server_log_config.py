import logging
from logging.handlers import TimedRotatingFileHandler
from .decorator import log

logging.basicConfig(level='INFO')
logger = logging.getLogger('server')


@log
def server_log(data):
    filename = 'client_server.log'
    handler = logging.FileHandler(filename)

    format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
    handler.setFormatter(format_)

    handler_2 = TimedRotatingFileHandler(filename, when="midnight", interval=1, backupCount=7)
    handler_2.suffix = "%Y-%m-%d"
    logger.addHandler(handler)
    logger.info(data)
    logger.addHandler(handler_2)
