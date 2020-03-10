""" etat des lieux:
- il faut enlever les templates de api.py au fur et à mesure
- utiliser requests.get_json() pour réussir à récuperer les données de l'utilisateur à partir du front-end (comme avec postman! reprendre code initial)
- vérifier que la communication front-back se fait bien: récupérer codes, récuperer infos
- il faut intégrer les nouveaux templates aux différents URL de l'application
- gérer les contrib (pb avec les parametres jinja)
"""

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


@app.route('/signup', methods=['POST'])
def signup_post():
    # Ajout d'un utilisateur dans la base de données
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "" or password == "":
        # Si un champ est vide
        flash('Password or username missing')
        return redirect(url_for('signup'))
    else:
        user = {"username": username, "password": password}
        r_signup = requests.post("http://ceptyconsultant.local:8000/signup", data=user)
        if r_signup.status_code == 201:
            return redirect(url_for('login'))
        elif r_signup.status_code == 226:
            flash('Username already exists')
            return redirect(url_for('signup'))


@app.route('/logout')
# @auth.login_required
def logout():
    # Déconnexion de l'utilisateur
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('index'))


# GET
@app.route('/contributions', methods=["GET"])
# @auth.login_required
def contrib():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    r = requests.get('http://ceptyconsultant.local:8000/api/resource/get')
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.status_code)
        print(r.text)
        return render_template("contrib.html", logged=session.get('logged_in'), params=r.json)
    else:
        return "PROBLEM"


@app.route('/get', methods=["GET"])
def get():
    r = requests.get('http://ceptyconsultant.local:8000/api/resource/get')
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.text)
    return "<p>"+str(r.json)+"<p>"

    """ autres requetes

# POST
@app.route('/add_contrib')
def post():
    if session.get('logged_in'):
        return render_template("ajout.html", logged=session.get('logged_in'))

@app.route('/add_contrib', methods=["POST"])
def post_contrib():
    #changer avec formulaire
    username = request.form.get('username')
    password = request.form.get('password')
    r = requests.post('http://ceptyconsultant.local:8000/api/resource/add_contrib', data=)
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.text)
    return "<p>"+str(r.json)+"<p>"

# PUT

@app.route('/update_contrib')
def put():
    if session.get('logged_in'):
        return render_template("modif.html", logged=session.get('logged_in'))

@app.route('/update_contrib', methods=["PUT"])
def put_contrib():
    #changer avec formulaire
    username = request.form.get('username')
    password = request.form.get('password')
    r = requests.put('http://ceptyconsultant.local:8000/api/resource/update_contrib', data=)
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.text)
    return "<p>"+str(r.json)+"<p>"

# DELETE
@app.route('/delete_contrib')
def delete():
    if session.get('logged_in'):
        return render_template("delete.html", logged=session.get('logged_in'))

@app.route('/delete_contrib', methods=["DELETE"])
def delete_contrib():
    #changer
    username = request.form.get('username')
    password = request.form.get('password')
    r = requests.delete('http://ceptyconsultant.local:8000/api/resource/delete_contrib', data=)
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.text)
    return "<p>"+str(r.json)+"<p>"




if __name__ == "__main__":
    app.run()
