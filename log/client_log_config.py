import logging
from .decorator import log


@log
def client_log(data):
    logging.basicConfig(level='INFO')
    logger = logging.getLogger('client')

    filename = 'client_server.log'
    handler = logging.FileHandler(filename)

    format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
    handler.setFormatter(format_)
    logger.addHandler(handler)
    logger.info(data)
