from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

#Page principale, renvoie à la page de login si l'on est pas déjà connecté
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Login correct"
        
#Page login (username = admin, password = password)
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    # renvoie la même page jusqu'à ce que l'user aie le bon login
    else:
        flash('wrong password!')
    return home()

#définit une clé secrète, nécessaire à l'éxécution
app.secret_key = os.urandom(12)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
