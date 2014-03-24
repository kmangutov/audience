
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from db_util import get_db, query_db, exec_db
from audience import app
from user_management import exists_account

SQL_ENTRY_EXISTS = 'select * from entries where entry_url=? limit 1'
SQL_ENTRY_INSERT = 'insert into entries(entry_url) values(?)'
SQL_SHARE = 'insert into shares(share_source, share_value) values(?, ?)'
SQL_USER_WALL = ('select * from shares '
 	'inner join users p1 '
 	'on p1.user_id=shares.share_source ' 
 	'inner join entries p2 '
 	'on p2.entry_id=shares.share_value '
 	'where p1.user_login=?')
SQL_ALL_WALL = ('select * from shares '
 	'inner join users p1 '
 	'on p1.user_id=shares.share_source ' 
 	'inner join entries p2 '
 	'on p2.entry_id=shares.share_value ')

# view all
@app.route('/')
def view_all():

	username = ""
	if session.get('logged_in'):
		username = session.get('username')

	entries = query_wall()
	return render_template('user.html', name=username, entries=entries)

# post a music entry by the user
@app.route('/u/<username>', methods=['POST'])
def add_entry(username):
    if not session.get('logged_in'):
        abort(401)

    if not session.get('username') == username:
    	# trying to post to a different person account
    	abort(401)

    url = request.form['url']
    do_share(username, url)

    return redirect(url_for('show_user', username=username))

def get_entry_id(url):
	entry = query_db(SQL_ENTRY_EXISTS, [url], one=True)
	
	if entry is None:
		# this is a new url
		return None
	else:
		return entry['entry_id']

def post_entry(url):

    entry = exec_db(SQL_ENTRY_INSERT, [url], one=True)
    return entry

def do_share(username, url):

	#check if url is already an entry in 'entries'
	#if it isnt add (url) into 'entries'
	#put into shares (user_id, entry_id)

	entry_id = get_entry_id(url)
	if entry_id is None:
		entry_id = post_entry(url)

	user_id = exists_account(username)

	entry = exec_db(SQL_SHARE, [user_id, entry_id])

def query_wall():
	entries = query_db(SQL_ALL_WALL)
	return entries;

def query_user_wall(username):
	entries = query_db(SQL_USER_WALL, [username])
	return entries;



# show the music entries this user has shared
@app.route('/u/<username>')
def show_user(username):
	entries = query_user_wall(username)
	return render_template('user.html', name=username, entries=entries)