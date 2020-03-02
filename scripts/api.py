import os
import datetime

from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask import make_response, flash, redirect, render_template, session

# Importation des modules pour l'authentification et la sécurité des mots de passe
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context # password hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired) # token

import wrangling_json_data as js

# Constructeur de l'API / initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# Extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Base de données des utilisateurs
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        """ Cryptage des mots de passe """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """ Concordance du mot de passe entré avec le mot de passe crypté """
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        """ Génération d'un token d'authentification avec expiration """
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod # l'utilisateur n'est connu que lorsque le token est décodé
    def verify_auth_token(token):
        """ Vérification de la validité et de la non expiration du token d'authentification """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # token valide, mais expiré
        except BadSignature:
            return None    # token invalide
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    """ il recherche le token dans le champ username d'abord puis s'il ne le trouve pas (le champ password est ignoré), il vérifie le username/password """
    # essai d'authentification par token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # essai d'authentification par username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

""" Partie pour le Front-End """

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html', logged=session.get('logged_in'))

# Page de profile
@app.route('/profile')
@auth.login_required # l'accès n'est autorisé que pour les utilisateurs authentifiés
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('profile.html', name=session.get('username'), logged=session.get('logged_in'))

# Page d'authentification qui apparait aux personnes non connectées
@app.route('/login')
def login():
    # if session.get('logged_in'):
        # return redirect(url_for('profile'))
    return render_template('login.html', logged=session.get('logged_in'))

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    # Rafraichit la page si l'utilisateur n'existe pas ou si le mot de passe ne correspond pas
    if not user or not verify_password(username, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) 
    
    # Si l'identifiant et le mot de passe entrés sont correct
    session['logged_in'] = True
    session['username'] = username
    return redirect(url_for('profile'))

# Page d'inscription qui apparait aux personnes non connectées
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
    if User.query.filter_by(username=username).first() is not None:
        # Si l'utilisateur existe déjà dans la base de données
        flash('Username already exists')
        return redirect(url_for('signup'))
    
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('login'))

@app.route('/logout')
@auth.login_required
def logout():
    # Déconnexion de l'utilisateur
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('index'))

# Page des contributions
@app.route('/contributions', methods=["GET"])
@auth.login_required
def contrib():
    data = js.read_data(js.path_all)
    return render_template("contrib.html", logged=True, params=data)

""" Partie pour l'API """

@app.route('/api/users', methods=['POST'])
def new_user():
    # Ajout d'un nouvel utilisateur
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # champ manquant
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # utilisateur existant déjà
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users/<int:id>')
def get_user(id):
    # Renvoie le nom d'utilisateur
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    # Renvoie le token d'authentification qui doit être mis dans le champ "Username" avec le type "Basic Auth" sur Postman
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    # Renvoie un message de salutation à l'utilisateur
    return jsonify({'data': 'Hello, %s!' % g.user.username})


# POST: Permet d'ajouter une contribution à la BD
@app.route("/api/resource/add_contrib", methods=["POST"])
@auth.login_required
def json_post():
    # vérification du format de la requête (JSON + clés requises)
    if request.is_json:
        req = request.get_json()
        if sorted(list(req.keys())) == sorted(js.required_write_keys):
            response_body = {
                "message": "JSON received!",
                "sender": req.get("user_name"),
                "timestamp": datetime.datetime.now(),
                "contrib_name": req.get("contrib_name")
            }
            js.write_data(req, js.path_all)
            res = make_response(jsonify(response_body), 200)
            return res
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

# GET: Permet de parser le fichier JSON pour consulter des données (ici, toutes)
@app.route("/api/resource/get", methods=["GET"])
@auth.login_required
def json_read():
    data = js.read_data(js.path_all)
    return make_response(jsonify(data))

# GET: l'ajout du nombre x dans l'url permet d'accéder à la contribution numéro x
@app.route("/api/resource/get/<int:num>", methods=["GET"])
@auth.login_required
def json_read_num(num):
    data = js.read_data(js.path_all)
    data = data[num]
    return make_response(jsonify(data))

# GET: l'ajout du champ y dans l'url permet d'accéder à ce champ dans toutes les contributions
@app.route("/api/resource/get/<string:field>", methods=["GET"])
@auth.login_required
def json_read_field(field):
    data = js.read_data(js.path_all)
    fields = []
    for i in data:
        fields.append(i[field])
    return make_response(jsonify(fields))

# GET: l'ajout du nombre x + champ y dans l'url permet d'accéder au champ y de la contribution x
@app.route("/api/resource/get/<int:num>/<string:field>", methods=["GET"])
@auth.login_required
def json_read_num_field(num, field):
    data = js.read_data(js.path_all)
    data = data[num][field]
    return make_response(jsonify(data))

# PUT: Modifie la valeur d'un champ dans une contribution donnée. Si aucun numéro de contribution n'est indiqué, le champ sera modifié dans toutes les contributions
@app.route("/api/resource/update_contrib", methods=["PUT"])
@auth.login_required
def json_updated():
    if request.is_json:
        req = request.get_json()
        if sorted(req.keys()) == sorted(js.required_update_keys):
            category = req["field"]
            data_number = req["data_number"]
            new_data = req["new_data"]
            js.update_data(category, new_data, js.path_all, data_number=None)
            response_body = {
                "message": "Data successfully updated!",
                "timestamp": datetime.datetime.now(),
                "field": category,
                "data_number": data_number,
                "new_data": new_data
            }
            res = make_response(jsonify(response_body), 200)
            return res
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_update_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

# DELETE: efface la contribution numéro x (x donné dans la requête)
@app.route("/api/resource/delete_contrib", methods=["DELETE"])
@auth.login_required
def json_delete():
    if request.is_json:
        req = request.get_json()
        if sorted(req.keys()) == sorted(js.required_delete_keys):
            data_number = req["data_number"]
            js.delete_data(data_number, js.path_all)
            response_body = {
                "message": "Data successfully deleted!",
                "timestamp": datetime.datetime.now(),
                "data_deleted": req
            }
            res = make_response(jsonify(response_body), 200)
            return res
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_delete_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

if __name__ == '__main__':
    # Création de la base de données des utilisateurs si elle n'existe pas
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
