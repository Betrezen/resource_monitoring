import json

from flask import Flask
from flask import render_template, redirect, url_for, request, flash, make_response

# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext import admin
# from flask.ext.admin.contrib import sqla
# from flask.ext.admin.contrib.sqla import filters
from flask_login import LoginManager
from flask_restful import Api

from pylib.pylib import get_random_uuid
from pylib.settings import SQLALCHEMY_DATABASE_URI
from pylib.settings import FLASK_SESSION_TYPE, FLASK_UPLOAD_FOLDER
from pylib.settings import FLASK_ALLOWED_EXTENSIONS, FLASK_RESOURCE_STATUSES
from pylib.db import DbProxy
from pylib.services import run_services