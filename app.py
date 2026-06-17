from flask import Flask, render_template, request, redirect, url_for, session
from argon2 import PasswordHasher   
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
ph = PasswordHasher()
app.secret_key = os.getenv('SECRET_KEY')

def logged():
    return 'logged_in' in session and session['logged_in']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if not logged():
        return redirect(url_for('index'))

    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    access_key_hash = os.getenv('ACCESS_KEY_HASH')

    try:
        ph.verify(access_key_hash, password)
        session['logged_in'] = True
        return redirect(url_for('home'))

    except VerifyMismatchError:
        msg = "Senha incorreta. Tente novamente."
        return render_template('index.html', msg=msg)   
    

if __name__ == '__main__':
    app.run(debug=True)