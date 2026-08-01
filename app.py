from createdb import get_db
from flask import Flask, render_template, request, redirect, url_for, session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
ph = PasswordHasher()
app.secret_key = os.getenv('SECRET_KEY')


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


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


@app.route('/adicionar-cartao')
def add_card_page():
    if not logged():
        return redirect(url_for('index'))

    return render_template('add_card.html')


@app.route('/editar-cartoes')
def edit_card_page():
    if not logged():
        return redirect(url_for('index'))

    return render_template('edit_card.html')


@app.route('/editar-emais')
def edit_email_page():
    if not logged():
        return redirect(url_for('index'))

    return render_template('edit_email.html')


@app.route('/enviar-emais')
def send_email_page():
    if not logged():
        return redirect(url_for('index'))

    return render_template('send_email.html')


@app.post('/login')
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


@app.post('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.post('/add_card')
def add_card():
    conn = get_db()
    cursor = conn.cursor()

    codigo = request.form['codigo']
    descricao = request.form['descricao']
    qtd_pecas = request.form['qtd_pecas']
    qtd_cartoes = request.form['qtd_cartoes']

    cursor.execute(
        'SELECT codigo FROM cartoes WHERE codigo = ?',
        (codigo,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        cursor.execute(
            'INSERT INTO cartoes (codigo, descricao, qtd_pecas, qtd_cartoes) VALUES (?, ?, ?, ?)',
            (codigo, descricao, qtd_pecas, qtd_cartoes)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    else:
        conn.close()
        msg = "Cartão já salvo no sistema."
        return render_template('add_card.html', msg=msg)


@app.get('/search_card')
def search_card():
    conn = get_db()
    cursor = conn.cursor()

    codigo = request.args['buscar_cartao']

    cursor.execute(
        'SELECT * FROM cartoes WHERE codigo = ?',
        (codigo,)
    )

    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        msg = "Código inexistente."
        return render_template('edit_card.html', msg=msg)

    return render_template('edit_card.html', cartao=resultado)


@app.post('/edit_card')
def edit_card():
    conn = get_db()
    cursor = conn.cursor()

    id_card = request.form['id']
    codigo = request.form['codigo_editado']
    descricao = request.form['descricao_editada']
    qtd_pecas = request.form['qtd_pecas_editada']
    qtd_cartoes = request.form['qtd_cartoes_editada']

    cursor.execute(
        'UPDATE cartoes SET codigo = ?, descricao = ?, qtd_pecas = ?, qtd_cartoes = ? WHERE id = ?',
        (codigo, descricao, qtd_pecas, qtd_cartoes, id_card)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('edit_card_page'))


@app.post('/delete_card')
def delete_card():
    conn = get_db()
    cursor = conn.cursor()

    id_card = request.form['id']

    cursor.execute(
        'DELETE FROM cartoes WHERE id = ?',
        (id_card,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('edit_card_page'))


if __name__ == '__main__':
    app.run(debug=False)