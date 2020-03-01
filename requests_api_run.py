from flask import Flask
from flask import request, jsonify, make_response, flash, redirect, render_template, session, abort
from flask_restful import Api
from flask import Response
import datetime
import wrangling_json_data as js

# python3.7 -m pip install Flask-HTTPAuth
# Importation des modules pour l'authentification et la sécurité des mots de passe
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
def index():
    return "Ceptyconsultant says Hello"

#contribution
@app.route("/contribution", methods=["GET"])
def contrib():
    data = js.read_data(js.path_all)
    return render_template("contributions.html", params=data)

#Login
@app.route("/login", methods=["GET"])
#@auth.login_required # l'accès n'est autorisé que pour les utilisateurs authentifiés
def login():
    return render_template("login.html")
    #return "Hello, %s!" % auth.username()


@app.route("/login", methods=["POST"])
#@auth.login_required # l'accès n'est autorisé que pour les utilisateurs authentifiés
def login2():
    other = request.form
    print(other)
    return "Bienvenue!"
    #return "Hello, %s!" % auth.username()

# POST: Permet d'ajouter une contribution à la BD
@app.route("/add_contrib", methods=["POST"])
@auth.login_required
def json_post():
    # vérification du format de la requête (JSON + clés requises)
    if request.is_json:
        req = request.get_json()
        if sorted(list(req.keys())) == sorted(js.required_write_keys):
            response_body = {
                "message": "contribution received!",
                "sender": req.get("user_name"),
                "timestamp": datetime.datetime.now(),
                "contrib_name": req.get("contrib_name")
            }
            js.write_data(req, js.path_all)
            res = make_response(jsonify(response_body), 200)
            return res
        else:
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: " + str(js.required_keys)}), 400)
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
@app.route("/update_contrib", methods=["PUT"])
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
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: " + str(js.required_update_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


# DELETE: efface la contribution numéro x (x donné dans la requête)
@app.route("/delete_contrib", methods=["DELETE"])
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
            return make_response(jsonify({"message": "Wrong data structure, check these fields exist in your request: " + str(js.required_delete_keys)}), 400)
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")