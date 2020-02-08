# record log by fyang
import logging.config


HOME_PATH = "".join([_ + "/" for _ in __file__.split("/")[:-1]])[:-1]
logging.basicConfig(
    filename=f'{HOME_PATH}/log',
    level=logging.DEBUG,
    format='%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


logger = logging
