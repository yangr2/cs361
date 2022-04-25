from flask import Flask, render_template, json, request, session, redirect
from flask_mysqldb import MySQL
from database import MYSQL_PASSWORD
import hashlib
import os   
import MySQLdb.cursors
import re
import urllib.request, json
import certifi
import ssl


# Configuration
app = Flask(__name__)

app.secret_key = '1122334455'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

# Routes
@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        if session and session['username']:
            return render_template("registered.j2", username = session['username'])
        else:
            return render_template("register.j2")
        
    msg = ''
    returnCode = '002'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'state' in request.form :
        username = request.form['username']
        password = request.form['password']
        state = request.form['state']
        
        # If user selects to input city name, check if the city cell has been filled.
        if request.form['localType'] == "city":
            if 'city' in request.form:
                city = request.form['city']
                zip_code = None
            else:
                msg = 'City is missing!!'
        
        # If user selects to input zip code, check if the zip cell has been filled.
        if request.form['localType'] == "zip":
            if 'zip' in request.form:
                zip_code = request.form['zip']
                city = None
            else:
                msg = 'Zip is missing'
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        if account:
            msg = 'The username existed. Please try another.'
        elif regex.search(username) != None:
            msg = 'Username must contain only characters and numbers!'
        else:
            hashed_string = hashlib.sha256(password.encode('utf-8')).hexdigest()
            cursor.execute('INSERT INTO accounts(username, password, state, city, zip_code) VALUES (% s, % s, % s, % s, %s)', (username, hashed_string, state, city, zip_code))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            session['loggedin'] = True
            session['username'] = username
            returnCode = "001"
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        
    if returnCode == "001":
        return render_template("registered.j2", username = username)
    else:
        return render_template("register.j2", msg = msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session and session['username']:
            return redirect("account")
        else:
            return render_template("login.j2")
        
    msg = ''
    returnCode = '002'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        if account:
            hashed_string = hashlib.sha256(password.encode('utf-8')).hexdigest()
            cursor.execute('SELECT * FROM accounts WHERE username = % s and password = % s', (username, hashed_string))
            account = cursor.fetchone()
            if account:
                msg = 'You have successfully registered!'
                session['loggedin'] = True
                session['username'] = username
                returnCode = "001"
            else:
                msg = 'User name does not existed / Password incorrect.'
        else:
            msg = 'User name does not existed / Password incorrect.'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        
    if returnCode == "001":
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        return redirect("account")
    else:
        return render_template("login.j2", msg = msg)
    


@app.route('/daily')
def daily_weather():
    if session and session['username']:
        username = session['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            return render_template("daily.j2", account = account)
        else:
            return render_template("daily.j2", account = {})
    else: 
        return render_template("daily.j2", account = {})
            


@app.route('/help')
def help():
    return render_template("help.j2")

@app.route('/geocoding' , methods=['POST'])
def geo():
    data = request.json
    if 'zip' in data.keys():
        url = "https://api.openweathermap.org/data/2.5/weather?zip="+data['zip']+"&appid="+data['appID']+'&units=metric'
    else :
        url = "https://api.openweathermap.org/data/2.5/weather?q="+data['city']+","+data['state']+"&appid="+data['appID']+'&units=metric'
    
    response = urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    data = response.read()
    print(data)
    
    return data

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect("login")

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        if session and session['username']:
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                return render_template("account.j2", account = account)
            else:
                return redirect("login")
        else:
            return redirect("login")
    
    msg = ''
    returnCode = '002'
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        password = request.form['password']
        state = request.form['state']
        
        # If user selects to input city name, check if the city cell has been filled.
        if request.form['localType'] == "city":
            if 'city' in request.form:
                city = request.form['city']
                zip_code = None
            else:
                msg = 'City is missing!!'
        
        # If user selects to input zip code, check if the zip cell has been filled.
        if request.form['localType'] == "zip":
            if 'zip' in request.form:
                zip_code = request.form['zip']
                city = None
            else:
                msg = 'Zip is missing'

        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        if account:
            if password:
                hashed_string = hashlib.sha256(password.encode('utf-8')).hexdigest()
                cursor.execute('UPDATE accounts set password =  % s WHERE username = % s', (hashed_string, username))
                mysql.connection.commit()
            if state:
                cursor.execute('UPDATE accounts set state =  % s WHERE username = % s', (state, username))
                mysql.connection.commit()
            if zip_code:
                cursor.execute('UPDATE accounts set zip_code =  % s, city = null WHERE username = % s', (zip_code, username))
                mysql.connection.commit()
            if city:
                cursor.execute('UPDATE accounts set city =  % s, zip_code = null WHERE username = % s', (city, username))
                mysql.connection.commit()
            returnCode = "001"
            msg = 'Information updated.'
        else:
            msg = 'Account does not existed!!'
            
    elif request.method == 'POST':
        msg = 'missing username'
    
    username = request.form['username']
    cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
    account = cursor.fetchone()
    if returnCode == "001":
        return render_template("account.j2", msg = msg, account = account, returnCode = returnCode)
    else:
        return render_template("account.j2", msg = msg, account = account, returnCode = returnCode)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    app.run(port=port, debug=True)