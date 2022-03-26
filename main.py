# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from flask_talisman import Talisman
import psycopg2
from urllib.parse import quote
from config import Config

app = Flask(__name__)
Talisman(app, content_security_policy=None)
app.secret_key = 'jkshefdhvjshvdf9w8erwuerhv'

# DATABASE
DATABASE_URI = Config.DATABASE_URI
conn = psycopg2.connect(DATABASE_URI)
cur = conn.cursor()

# http://localhost:5000/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        cur.execute('SELECT * FROM revise WHERE username = %s AND password = %s', (username, password,))
        account = cur.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[1]
            session['username'] = account[3]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        
        cur.execute('SELECT * FROM revise WHERE username = %s', (session['username'],))
        account = cur.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/results - this will be the profile page, only accessible for loggedin users
@app.route('/results')
def results():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        cur.execute('SELECT * FROM results WHERE tg_id = %s', (session['id'],))
        results = cur.fetchall()
        res_list = []
        for result in results:
            temp_res = list(result)
            res_list.append(temp_res)

        # Show the results page with results table
        return render_template('results.html', results=res_list)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# DEBUG SERVER
if __name__ == '__main__':
    app.run(debug=True, port=5000)