import requests
from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask import make_response, flash, redirect, render_template, session

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

# Page d'authentification qui apparait aux personnes non connectées
@app.route('/login')
def login():
    #return "login"
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = {"username": username, "password": password}
    r_login = requests.post("http://ceptyconsultant.local:8000/login", data=user)
    if r_login.status_code == 200:
        return "welcome, "+str(username)+"!"
    else:
        return "incorrect login"


@app.route('/profile')
def profile():
    #return "login"
    return render_template('profile.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/contributions')
# @auth.login_required
def contrib():
    return render_template("contrib.html")


@app.route('/api/resource/get', methods=["GET"])
def get():
    r = requests.get('http://ceptyconsultant.local:8000/api/resource/get')
    print(r)
    print(r.json)
    print(r.status_code)
    print(r.text)
    return r.json




if __name__ == "__main__":
    app.run()
