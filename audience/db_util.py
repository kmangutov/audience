

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from audience import app

#some database stuffs

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def exec_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    get_db().commit()
    rv = cur.fetchall()
    cur.close()
    return cur.lastrowid
    #return (rv[0] if rv else None) if one else rv

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()