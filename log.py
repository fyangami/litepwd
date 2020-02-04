# record log by fyang
import logging.config


logging.basicConfig(
    filename='log',
    level=logging.DEBUG,
    format='%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def print_error(msg):
    logging.error(msg)


def print_warning(msg):
    logging.warning(msg)
