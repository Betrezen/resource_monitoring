# -*- python -*-
# author: krozin@gmail.com
# log: created 2016/02/01.
# copyright

import logging
import os

# create logger
logger = logging.getLogger('pipeline')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
stream_handler = logging.StreamHandler()
#file_handler = logging.FileHandler('log.log')
stream_handler.setLevel(logging.DEBUG)
#file_handler.setLevel(logging.DEBUG)


# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#formatter = logging.Formatter('%(message)s')

# add formatter to ch #stream_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
#file_handler.setFormatter(formatter)

# add stream_handler to logger
logger.addHandler(stream_handler)
#logger.addHandler(file_handler)

# Log level colors
logging.addLevelName(logging.DEBUG, "\033[1;34m{}\033[1;0m".format(logging.getLevelName(logging.DEBUG)))
logging.addLevelName(logging.INFO, "\033[1;32m{}\033[1;0m".format(logging.getLevelName(logging.INFO)))
logging.addLevelName(logging.WARNING, "\033[1;33m{}\033[1;0m".format(logging.getLevelName(logging.WARNING)))
logging.addLevelName(logging.ERROR, "\033[1;31m{}\033[1;0m".format(logging.getLevelName(logging.ERROR)))
logging.addLevelName(logging.CRITICAL, "\033[1;41m{}\033[1;0m".format(logging.getLevelName(logging.CRITICAL)))


def set_file(fname):
    fn = os.path.abspath(fname)
    file_handler = logging.FileHandler(fn)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.handlers = [file_handler, stream_handler]

