
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from db_util import get_db, query_db
from audience import app

SQL_ENTRY_EXISTS = 'select exists(select 1 from entries where entry_url=? limit 1)'
SQL_ENTRY_INSERT = 'insert into entries(entry_url) values(?)'
SQL_SHARE = 'insert into shares(share_source, share_value) values(?, ?)'

# post a music entry by the user
@app.route('/u/<username>', methods=['POST'])
def add_entry(username):
    if not session.get('logged_in'):
        abort(401)

    if not session.get('username') == username:
    	# trying to post to a different person account
    	abort(401)

    url = request.form['url']
    post_entry(url)

def get_entry_id(url):
	entry = query_db(SQL_ENTRY_EXISTS, [url], one=True)
	
	if entry is None:
		# this is a new url
		return None
	else:
		return entry['entry_id']

def post_entry(url):
    #db = get_db()
    #db.execute(SQL_ENTRY_INSERT, [url])
    #db.commit()

    entry = query_db(SQL_ENTRY_INSERT, [url], one=True)
    return entry['entry_id']

def do_share(username, url):

	#check if url is already an entry in 'entries'
	#if it isnt add (url) into 'entries'
	#put into shares (user_id, entry_id)

	entry_id = get_entry_id(url)
	if entry_id is None:
		entry_id = post_entry(url)

	#entry = query_db(SQL_SHARE, )

	pass

# show the music entries this user has shared
@app.route('/u/<username>')
def show_user(username):
    return render_template('user.html', name=username)