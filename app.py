from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import users
import produtos
import email_config
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_super_secreta")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuarios = users.carregar_usuarios()
        if email in usuarios:
            senha_hash = usuarios[email]
            if check_password_hash(senha_hash, senha):
                session['usuario'] = email
                try:
                    yag = yagmail.SMTP(email_config.EMAIL_USER, email_config.EMAIL_PASS)
                    yag.send(email, 'Login Realizado', 'Olá, você fez login com sucesso no painel.')
                except Exception as e:
                    print(f"Erro ao enviar email: {e}")
                return redirect(url_for('dashboard'))
        flash("Credenciais inválidas. Tente novamente.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        lista_produtos = produtos.carregar_produtos()
        return render_template('dashboard.html', usuario=session['usuario'], produtos=lista_produtos)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu com sucesso.")
    return redirect(url_for('login'))

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        usuarios = users.carregar_usuarios()
        if email in usuarios:
            try:
                yag = yagmail.SMTP(email_config.EMAIL_USER, email_config.EMAIL_PASS)
                link = f'https://painel-vendas-qktv.onrender.com/nova_senha?email={email}'
                yag.send(email, 'Recuperação de senha', f'Clique no link para redefinir sua senha: {link}')
                flash('Email para recuperação enviado.')
            except Exception as e:
                flash(f"Erro ao enviar email: {e}")
        else:
            flash('Email não cadastrado.')
    return render_template('recuperar_senha.html')

@app.route('/nova_senha', methods=['GET', 'POST'])
def nova_senha():
    email_query = request.args.get('email', '')
    if request.method == 'POST':
        email = request.form['email']
        nova_senha = request.form['nova_senha']
        confirmar = request.form['confirmar_senha']
        if nova_senha != confirmar:
            flash("As senhas não coincidem.")
            return render_template('nova_senha.html', email=email)
        usuarios = users.carregar_usuarios()
        if email in usuarios:
            usuarios[email] = generate_password_hash(nova_senha)
            users.salvar_usuarios(usuarios)
            flash("Senha atualizada com sucesso! Faça login.")
            return redirect(url_for('login'))
        else:
            flash("Email não encontrado.")
    return render_template('nova_senha.html', email=email_query)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        produtos.adicionar_produto(nome, preco, descricao)
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('dashboard'))
    return render_template('cadastrar_produto.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
