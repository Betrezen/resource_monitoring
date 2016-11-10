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


__NAME__ = "monoringOfResources"
ALLOWED_EXTENSIONS = set(FLASK_ALLOWED_EXTENSIONS)
STATUSES = set(FLASK_RESOURCE_STATUSES)

# Create application
app = Flask(__NAME__)
#, static_url_path = '/home/ubuntu/ocr/storage',
#                      static_folder = '/home/ubuntu/ocr/storage')

# Create dummy secrey key so we can use sessions
app.secret_key = get_random_uuid()
app.url_map.strict_slashes = False
app.config['SESSION_TYPE'] = FLASK_SESSION_TYPE
app.config['UPLOAD_FOLDER'] = FLASK_UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
api = Api(app)

# Create database
# db = SQLAlchemy(app)

# Create admin
login_manager = LoginManager()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {'content-type': 'application/xml'})
    return resp

# Routes
# Main pages
@app.route('/')
def resource_list_page():
    dbproxy = DbProxy()
    resources = dbproxy.get_all()
    # resources = Resource.query.all()
    context = {'resource': resources}
    return render_template('index.html', data=context)

@app.route('/new', methods=['GET'])
def resource_form():
    context = {'allowed': ALLOWED_EXTENSIONS,
               'statuses': STATUSES,
               'turnon': ['ON', 'OFF']}
    return render_template('add.html', data=context)

@app.route('/add', methods=['POST'])
def resource_add():
    if request.method == 'POST':
        dbproxy = DbProxy()
        name = request.form['name']
        turn = request.form['turnon']
        turnon = False
        if turn == 'ON':
            turnon = True
        status = request.form['status']
        href = request.form['href']
        dbproxy.add_resource(name=name, turnon=turnon, status=status, href=href)
        flash("Item: ID=[{}] has been created".format('NA'))
        return redirect(url_for('resource_list_page'))

@app.route('/delete/<rid>', methods=['DELETE', 'GET'])
def resource_del(rid=None):
    dbproxy = DbProxy()
    res = dbproxy.delete_resource(rid=rid)
    flash ("Item: ID=[{}] has been deleted".format(rid))
    return redirect(url_for('resource_list_page'))

@app.route('/edit/<rid>', methods=['GET'])
def resource_edit(rid=None):
    dbproxy = DbProxy()
    res = dbproxy.get_resource(rid)
    if res.turnon:
        res.turnon = 'ON'
    else:
        res.turnon = 'OFF'
    if res:
        context = {'resource': res, 'statuses': STATUSES, 'turnon': ['ON', 'OFF']}
    return render_template('edit.html', data=context)

@app.route('/update/<rid>', methods=['POST'])
def resource_update(rid=None):
    dbproxy = DbProxy()
    res = dbproxy.get_resource(rid)
    if res:
        turn = request.form['turnon']
        turnon = False
        if turn == 'ON':
            turnon = True
        status = request.form['status']
        href = request.form['href']
        dbproxy.update_resource(rid=rid, turnon=turnon, status=status, href=href)
    flash("Item: ID=[{}] has been updated. {}".format(rid, request.form['status']))
    return redirect(url_for('resource_list_page'))

@app.route('/help')
def help_page():
    return render_template('help.html')

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # run_services()
    app.run('127.0.0.1', 8989, debug=False)
