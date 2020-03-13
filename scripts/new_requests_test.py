# coding:utf-8
import requests
import os
from flask import Flask, abort, request, jsonify, g, url_for, Response
from flask import flash, redirect, render_template, session

import datetime
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12)


@app.route("/", endpoint="idx")
def index():
    return render_template("index.html", logged=session.get("logged_in"))

# Page d'authentification qui apparait aux personnes non connectees
@app.route("/login", endpoint="login")
def login():
    if session.get("logged_in"):
        return redirect(url_for("profile"))
    return render_template("login.html", logged=session.get("logged_in"))


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = {"username": username, "password": password}

    r_login = requests.post("http://ceptyconsultant.local:8000/login", json=user)

    print(r_login.text, r_login.status_code, r_login.json)
    if r_login.status_code == 200:
        # Si l'identifiant et le mot de passe entrés sont corrects
        session["logged_in"] = True
        session["username"] = username

        return redirect(url_for("profile"))
    else:
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))


@app.route("/profile", endpoint="profile")
def profile():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        return render_template(
            "profile.html",
            name=session.get("username"),
            logged=session.get("logged_in")
        )


@app.route("/signup")
def signup():
    if session.get("logged_in"):
        return redirect(url_for("profile"))
    return render_template("signup.html", logged=session.get("logged_in"))


@app.route("/signup", methods=["POST"])
def signup_post():
    # Ajout d'un utilisateur dans la base de données
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "" or password == "":
        # Si un champ est vide
        flash("Password or username missing")
        return redirect(url_for("signup"))
    else:
        user = {"username": username, "password": password}
        r_signup = requests.post("http://ceptyconsultant.local:8000/api/users", json=user)
        print("TEXT:",r_signup.text, "CODE:", r_signup.status_code, "JSON",r_signup.json)
        if r_signup.status_code == 201:
            return redirect(url_for("login"))
        elif r_signup.status_code == 409:
            flash("Username already exists")
            return redirect(url_for("signup"))
        else:
            return "Let's debug!"


@app.route("/logout")
# @auth.login_required
def logout():
    # Déconnexion de l'utilisateur
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("username", None)
    session["logged_in"] = False
    return redirect(url_for("idx"))


# GET
@app.route("/contributions", endpoint="contrib", methods=["GET"])
# @auth.login_required
def contrib():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    r = requests.get("http://ceptyconsultant.local:8000/api/resource/get")
    if r.status_code == 200:
        print(r)
        print(r.status_code)
        return render_template(
            "contrib.html", logged=session.get("logged_in"), params=r.json()
        )
    else:
        # TODO: à modifier
        print("TEXT:",r.text, "CODE:", r.status_code, "JSON",r.json)
        return "PROBLEM"


@app.route("/get", methods=["GET"])
def get():
    r = requests.get("http://ceptyconsultant.local:8000/api/resource/get")
    if r.status_code == 200:
        print(r)
        print(r.text)
        return "Done!"
    # TODO; à modifier, gestion des erreurs
    return "<p>" + str(r.json) + "<p>"


# POST
@app.route("/add_contrib", endpoint="post")
def post():
    if session.get("logged_in"):
        return render_template("ajout.html", logged=session.get("logged_in"))
    return redirect(url_for("login"))


@app.route("/add_contrib", methods=["POST"])
def post_contrib():
    user_name = session.get("username")
    last_update = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    validate = request.form.get("validate")
    contrib_type = request.form.get("contrib_type")
    contrib_data = request.form.get("contrib_data")
    contrib_path = request.form.get("contrib_path")
    contrib_name = request.form.get("contrib_name")
    ntealan = request.form.get("ntealan")

    contrib = {
        "contrib_data": contrib_data,
        "contrib_name": contrib_name,
        "contrib_path": contrib_path,
        "contrib_type": contrib_type,
        "last_update": last_update,
        "ntealan": ntealan,
        "user_name": user_name,
        "validate": validate,
    }
    r = requests.post(
        "http://ceptyconsultant.local:8000/api/resource/add_contrib", json=contrib
    )
    print(r.status_code)
    # print(r.text)
    if r.status_code == 200:
        # print(r)
        # print(r.text)
        return render_template("success_ajout.html", logged=session.get("logged_in"))
    # TODO; à modifier, gestion des erreurs
    flash("Unexpected error. Please try again.")
    return redirect(url_for("post"))


# PUT


@app.route("/update_contrib", endpoint="put")
def put():
    if session.get("logged_in"):
        return render_template("modif.html", logged=session.get("logged_in"))
    return redirect(url_for("login"))


@app.route("/update_contrib", methods=["POST"])
def put_contrib():
    # changer avec formulaire
    print("UPDATE CONTRIBUTION")
    field = request.form.get("change_input")
    number = request.form.get("change_id")
    new_data = request.form.get("change_modif")

    contrib = {"field": field, "data_number": number, "new_data": new_data}

    r = requests.put(
        "http://ceptyconsultant.local:8000/api/resource/update_contrib", json=contrib
    )
    print(r.status_code)
    print(r.text)
    if r.status_code == 200:
        print(r)
        print(r.text)
        return render_template("success_modif.html", logged=session.get("logged_in"))
    # TODO; à modifier, gestion des erreurs
    else:
        flash("Please check you have a correct ID and try again.")
        return redirect(url_for("put"))

# DELETE
@app.route("/delete_contrib", endpoint="delete")
def delete():
    if session.get("logged_in"):
        return render_template("delete.html", logged=session.get("logged_in"))
    return redirect(url_for("login"))


@app.route("/delete_contrib", methods=["POST"])
def delete_contrib():
    print("DELETE CONTRIBUTION")
    public_id = request.form.get("contrib_name")
    contrib = {"public_id": public_id}
    r = requests.delete(
        "http://ceptyconsultant.local:8000/api/resource/delete_contrib", json=contrib
    )
    print(r.status_code)
    print(r.text)
    if r.status_code == 200:
        print(r)
        print(r.text)
        return render_template("success_delete.html", logged=session.get("logged_in"))
    # TODO; à modifier, gestion des erreurs
    else:
        flash("Please check your public_id is correct and try again.")
        return redirect(url_for("delete"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
