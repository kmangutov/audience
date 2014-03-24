
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from db_util import get_db

from audience import app

QL_USER_EXISTS = 'select exists(select 1 from users where user_login=? limit 1)'
SQL_USER_INSERT = 'insert into users(user_login, user_pass) values(?,?)'
SQL_USER_LOGIN = 'select exists(select 1 from users where user_login=? and user_pass=? limit 1)'

#def exists_entry(url):


@app.route('/u/<username>', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    url = request.form['url']
    post_entry(url)



#def post_entry(url):



@app.route('/u/<username>')
def show_user(username):
    return render_template('user.html', name=username)