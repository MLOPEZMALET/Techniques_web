import requests
import os
from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask import make_response, flash, redirect, render_template, session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)


@app.route('/')
def index():
    return render_template('index.html', logged=session.get('logged_in'))

# Page d'authentification qui apparait aux personnes non connectées
@app.route('/login')
def login():
    if session.get('logged_in'):
        return redirect(url_for('profile'))
    return render_template('login.html', logged=session.get('logged_in'))


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = {"username": username, "password": password}
    r_login = requests.post("http://ceptyconsultant.local:8000/login", data=user)
    if r_login.status_code == 200:
        # Si l'identifiant et le mot de passe entrés sont correct
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('profile'))
        #return "welcome, "+str(username)+"!"
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('profile.html', name=session.get('username'), logged=session.get('logged_in'))


@app.route('/signup')
def signup():
    if session.get('logged_in'):
        return redirect(url_for('profile'))
    return render_template('signup.html', logged=session.get('logged_in'))

@app.route('/logout')
# @auth.login_required
def logout():
    # Déconnexion de l'utilisateur
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/contributions')
# @auth.login_required
def contrib():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = js.read_data(js.path_all)
    return render_template("contrib.html", logged=session.get('logged_in'), params=data)


@app.route('/get', methods=["GET"])
def get():
    r = requests.get('http://ceptyconsultant.local:8000/api/resource/get')
    print(r)
    print(r.json)
    print(r.status_code)
    print(r.text)
    return "<p>"+str(r.json)+"<p>"


if __name__ == "__main__":
    app.run()
