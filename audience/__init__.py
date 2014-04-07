
import os
import sqlite3
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash



# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)




# import my modules
from db_util import get_db
import audience.user_management
import audience.entry_management



