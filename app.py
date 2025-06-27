from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import users
import yagmail
import email_config

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

                # Enviar e-mail ao logar
                yag = yagmail.SMTP(email_config.email_remetente, email_config.senha_app)
                assunto = "Login detectado no Painel de Vendas"
                corpo = f"Usuário {email} acabou de logar com sucesso no sistema."
                yag.send(email_config.email_destino, assunto, corpo)

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
