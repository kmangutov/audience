
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from db_util import get_db

from audience import app


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        # if this is a login attempt,

        username = request.form['username']
        password = request.form['password']

        if exists_account(username):
            if valid_login(username, password):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash('Logged in!')
                return redirect(url_for('show_user', username=username))
                
            error = "Invalid password"
            return render_template('login.html', error=error)

        error = "Invalid login name"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        # if this is a register attempt,

        username = request.form['username']
        password = request.form['password']

        if exists_account(username):
            flash("Username already exists")
            return redirect(url_for('register'))
        
        create_account(username, password)
        flash("Account created")

        session['logged_in'] = True
        session['username'] = request.form['username']

        return redirect(url_for('show_user', username=username))

    return render_template('register.html')




##########################################
##########################################database stuff

SQL_USER_EXISTS = 'select exists(select 1 from users where user_login=? limit 1)'
SQL_USER_INSERT = 'insert into users(user_login, user_pass) values(?,?)'
SQL_USER_LOGIN = 'select exists(select 1 from users where user_login=? and user_pass=? limit 1)'

def valid_login(username, password):
    db = get_db()
    cur = db.execute(SQL_USER_LOGIN, [username, password])
    value = cur.fetchone()

    #check that len(result) is 1 to be valid
    return value[0] == 1

def create_account(username, password):
    db = get_db()
    db.execute(SQL_USER_INSERT, [username, password])
    db.commit()


def exists_account(username):
    #check if exists
    db = get_db()
    cur = db.execute(SQL_USER_EXISTS, [username])
    value = cur.fetchone()

    app.logger.debug(value[0])

    #check that len(result) is 1 to be valid
    return value[0] == 1
##############################################
##############################################

