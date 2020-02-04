from flask import Flask
from flask import request, jsonify, make_response, flash, redirect, render_template, session, abort
from flask_restful import Api
import wrangling_json_data as js
import os

# python3.7 -m pip install Flask-HTTPAuth
# Importation des module pour l'authentification et la sécurité des mots de passe
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# Constructeur de l'API
app = Flask(__name__)
api = Api(app)

auth = HTTPBasicAuth()

# Base de donnée des utilisateurs
users = {
    "Mikolov": generate_password_hash("password"),
    "Bergier": generate_password_hash("password"),
    "Taken": generate_password_hash("password"),
    "Gate": generate_password_hash("password"),
    "Fokwe": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

# Page d'accueil
@app.route("/")
@auth.login_required # l'accès n'est autorisé que pour les utilisateurs authentifiés

def index():
    return "Hello, %s!" % auth.username()

# POST: Permet d'ajouter une contribution à la BD
@app.route("/", methods=["POST"])
@auth.login_required
def json_post():
    # vérification du format de la requête (JSON + clés requises)
    if request.is_json:
        req = request.get_json()
        if sorted(list(req.keys())) == sorted(js.required_write_keys):
            response_body = {
                "message": "JSON received!",
                "sender": req.get("user_name")
            }
            js.write_data(req, js.path_all)
            res = make_response(jsonify(response_body), 200)
            return res
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


# GET: Permet de parser le fichier JSON pour consulter des données (ici, toutes)
@app.route("/get", methods=["GET"])
@auth.login_required
def json_read():
    data = js.read_data(js.path_all)
    return make_response(jsonify(data))


# GET: l'ajout du nombre x dans l'url permet d'accéder à la contribution numéro x
@app.route("/get/<int:num>", methods=["GET"])
@auth.login_required
def json_read_num(num):
    data = js.read_data(js.path_all)
    data = data[num]
    return make_response(jsonify(data))

# GET: l'ajout du champ y dans l'url permet d'accéder à ce champ dans toutes les contributions
@app.route("/get/<string:field>", methods=["GET"])
@auth.login_required
def json_read_field(field):
    data = js.read_data(js.path_all)
    fields = []
    for i in data:
        fields.append(i[field])
    return make_response(jsonify(fields))


# GET: l'ajout du nombre x + champ y dans l'url permet d'accéder au champ y de la contribution x
@app.route("/get/<int:num>/<string:field>", methods=["GET"])
@auth.login_required
def json_read_num_field(num, field):
    data = js.read_data(js.path_all)
    data = data[num][field]
    return make_response(jsonify(data))


# PUT: Modifie la valeur d'un champ dans une contribution donnée. Si aucun numéro de contribution n'est indiqué, le champ sera modifié dans toutes les contributions
@app.route("/", methods=["PUT"])
@auth.login_required
def json_updated():
    if request.is_json:
        req = request.get_json()
        if sorted(req.keys()) == sorted(js.required_update_keys):
            category = req["field"]
            data_number = req["data_number"]
            new_data = req["new_data"]
            js.update_data(category, new_data, js.path_all, data_number=None)
            return "Data successfully updated!"
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_update_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


# DELETE: efface la contribution numéro x (x donné dans la requête)
@app.route("/", methods=["DELETE"])
@auth.login_required
def json_delete():
    if request.is_json:
        req = request.get_json()
        if sorted(req.keys()) == sorted(js.required_delete_keys):
            data_number = req["data_number"]
            js.delete_data(data_number, js.path_all)
            return "Data successfully deleted!"
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: "+ str(js.required_delete_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)
    
if __name__ == '__main__':
    app.run(debug=True, port=8888)
