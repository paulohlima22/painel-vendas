
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import users
import email_config
import yagmail
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email in users.users:
            senha_hash = users.users[email]
            if check_password_hash(senha_hash, senha):
                session['usuario'] = email
                return redirect(url_for('dashboard'))
        return "Credenciais inválidas. Tente novamente."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        if email in users.users:
            yag = yagmail.SMTP(email_config.email_remetente, email_config.senha_app)
            assunto = "Recuperação de senha - Painel de Vendas"
            corpo = f"Olá, {email}. Recebemos sua solicitação para recuperar a senha.\n\nSua senha não pode ser recuperada por segurança, mas você pode redefinir com o admin."
            yag.send(to=email, subject=assunto, contents=corpo)
            return "E-mail de recuperação enviado com sucesso!"
        else:
            return "E-mail não encontrado."
    return render_template('recuperar.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
