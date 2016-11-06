# -*- python -*-
# author: krozin@gmail.com
# settings: created 2016/10/30.
# copyright

import os
import socket

from log import logger, set_file
from yamlloader import get_env

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.conf')
env = get_env(filepath=filepath,  attrdict=True)

##############################
# common #
##############################
ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    LOG_FILENAME = env.common.LOG_FILENAME
except:
    LOG_FILENAME = os.path.join(ROOT_FOLDER, 'results.log')


##############################
# Logging #
##############################
set_file(LOG_FILENAME)
LOGGER = logger
logger.debug("ROOT_FOLDER={}".format(ROOT_FOLDER))


##############################
# Services #
##############################
try:
    DBPATH = env.db.get('filepath')
except:
    DBPATH = os.path.join(ROOT_FOLDER, 'resources.db')

try:
    ZEROMQ_SERVER_HOST = env.zeromq_server.get('host')
    ZEROMQ_SERVER_PORT = int(env.zeromq_server.get('port'))
except:
    ZEROMQ_SERVER_HOST = socket.gethostname()
    ZEROMQ_SERVER_PORT = 9595

logger.debug("DBPATH={}".format(DBPATH))


##############################
# Flask #
##############################
try:
    FLASK_SESSION_TYPE = env.flask.get('session_type')
    FLASK_UPLOAD_FOLDER = env.flask.get('upload_folder')
    FLASK_ALLOWED_EXTENSIONS = env.flask.get('allowed_extensions')
    FLASK_RESOURCE_STATUSES = env.flask.get('statuses')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DBPATH)
except:
    FLASK_SESSION_TYPE = 'filesystem'
    FLASK_UPLOAD_FOLDER = './static/storage'
    FLASK_ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    FLASK_RESOURCE_STATUSES = ['OK', 'NOK', 'NA', 'XZ']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format('resources.db')

logger.debug("FLASK_SESSION_TYPE={}".format(FLASK_SESSION_TYPE))
logger.debug("FLASK_UPLOAD_FOLDER={}".format(FLASK_UPLOAD_FOLDER))
logger.debug("FLASK_ALLOWED_EXTENSIONS={}".format(FLASK_ALLOWED_EXTENSIONS))
logger.debug("FLASK_RESOURCE_STATUSES={}".format(FLASK_RESOURCE_STATUSES))