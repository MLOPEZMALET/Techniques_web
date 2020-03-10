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
    print(r_login.text, r_login.status_code, r_login.json)
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


# POST
@app.route('/add_contrib')
def post():
    if session.get('logged_in'):
        return render_template("ajout.html", logged=session.get('logged_in'))


@app.route('/add_contrib', methods=["POST"])
def post_contrib():
    user_id = request.form.get('user_id')
    article_id = request.form.get('article_id')
    user_name = session["username"]
    last_update = datetime.datetime.now()
    validate = request.form.get('validate')
    contrib_type = request.form.get('contrib_type')
    dico_id = request.form.get('dico_id')
    contrib_data = request.form.get('contrib_data')
    contrib_path = request.form.get('contrib_path')
    contrib_name = request.form.get('contrib_name')
    public_id = request.form.get('public_id')
    ntealan = True
    # quand modifié ntealan = request.form.get('ntealan')

    contrib = {
                "article_id": article_id,
                "contrib_data": "amm-2395b25e-2164-4c7d-a685-54a6c6e91f0d_1-2019-09-23T110018.479Z-.wav",
                "contrib_name": "ammɛ",
                "contrib_path": "https://ntealan.net/soundcontrib/",
                "contrib_type": "sound",
                "dico_id": "yb_fr_3031",
                "last_update": "2019-09-23 11:00:52.802000",
                "ntealan": true,
                "public_id": "d76514c3-d605-4f01-8284-a17031f9bf9f",
                "user_id": "b42e96a8-7b0b-8b45-ae69-7c2efd472e1d",
                "user_name": "Bergier",
                "validate": false
                }
    r = requests.post('http://ceptyconsultant.local:8000/api/resource/add_contrib', data=contrib)
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
    field = request.form.get('change_input')
    number = request.form.get('change_id')
    new_data = request.form.get('change_modif')
    contrib = {"field": field, "data_number": number, "new_data": new_data}
    r = requests.put('http://ceptyconsultant.local:8000/api/resource/update_contrib', data=contrib)
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
    public_id = request.form.get('contrib_name')
    contrib = {"public_id": public_id}
    r = requests.delete('http://ceptyconsultant.local:8000/api/resource/delete_contrib', data=contrib)
    if r.status_code == 200:
        print(r)
        print(r.json)
        print(r.text)
    return "<p>"+str(r.json)+"<p>"




if __name__ == "__main__":
    app.run()
