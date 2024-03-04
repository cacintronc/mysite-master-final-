#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""
from flask import Flask, render_template
from flask import redirect, url_for, request
from flask import session, flash
from flask import g
import sqlite3
from datetime import datetime

DEVELOPMENT_ENV = True

app = Flask(__name__)


app_data = {
    "name": "Best Buy Customers App",
    "description": "Making our Customers happy since 1966!",
    "author": "Best Buy",
    "html_title": "Best Buy",
    "project_name": "Best Buy",
    "keywords": "flask, webapp, tbasic",
}

# configs
app.secret_key = 'my precious' # tell me you have seen Lord of The Rings

# connect to database
def connect_db():
    return sqlite3.connect('sample.db')

app.database = 'sample.db'

from functools import wraps
# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('index'))
    return render_template('login.html', app_data=app_data, error=error)



@app.route("/")
def index():
    return render_template("index.html", app_data=app_data)


@app.route("/about")
def about():
    return render_template("about.html", app_data=app_data)


@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=app_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', app_data=app_data, error=error)

@app.route("/complains", methods=['GET', 'POST'])
@login_required
def complains():
    g.db = connect_db()
    username = session['username']
    cur = g.db.execute('SELECT userid FROM users WHERE username = ?', (username,))
    user_id = cur.fetchone()[0]
    if request.method == 'POST':
        complaint = request.form['complaint']
        thetime = datetime.now()
        g.db.execute('INSERT INTO complaints (user_id, complaint, time) VALUES (?, ?, ?)', (user_id, complaint, thetime,))
        g.db.commit()

    cur2 = g.db.execute('select * from complaints WHERE user_id = ?;', (user_id,))
    complaints = [dict(time=row[3], complaint=row[2]) for row in cur2.fetchall()]
    g.db.close()
    return render_template("complains.html", app_data=app_data, complaints=complaints)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    g.db = connect_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        g.db.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',  (username, password,))
        g.db.commit()
        session['logged_in'] = True
        session['username'] = request.form['username']
        flash('You were logged in.')
        return redirect(url_for('index'))
    return render_template('register.html', app_data=app_data)


if __name__ == "__main__":
     app.run(debug=DEVELOPMENT_ENV)