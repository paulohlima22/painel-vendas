from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask import abort
import users
import produtos
import anuncios
import email_config
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_super_secreta")

# 📁 Pasta onde as imagens dos anúncios serão salvas
UPLOAD_FOLDER = os.path.join('static', 'anuncios')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        lista_anuncios = anuncios.carregar_anuncios()
        return render_template('dashboard.html', usuario=session['usuario'], produtos=lista_produtos, anuncios=lista_anuncios)
    return redirect(url_for('login'))

@app.route('/meus_anuncios')
def meus_anuncios():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    email = session['usuario']
    todos = anuncios.carregar_anuncios()
    meus = [a for a in todos if a.get('email') == email]
    return render_template('meus_anuncios.html', anuncios=meus, usuario=email)

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
                flash('Email para recuperação enviado. Verifique sua caixa de entrada.')
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
        link = request.form['link']
        produtos.adicionar_produto(nome, preco, descricao, link)
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('dashboard'))
    return render_template('cadastrar_produto.html')

@app.route('/cadastrar_anuncio', methods=['GET', 'POST'])
def cadastrar_anuncio():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        anunciante = request.form['anunciante']
        descricao = request.form['descricao']
        link = request.form['link']
        imagem = request.files['imagem']

        if imagem:
            nome_arquivo = secure_filename(imagem.filename)
            caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            imagem.save(caminho_imagem)
        else:
            nome_arquivo = None

        email = session['usuario']
        anuncios.adicionar_anuncio(nome_produto, anunciante, descricao, link, nome_arquivo, email)
        flash('Anúncio cadastrado com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('cadastrar_anuncio.html')

@app.route('/anuncie')
def anuncie():
    return render_template('anuncie.html')

# ===== Rotas adicionadas para editar e excluir anúncios =====

@app.route('/editar_anuncio/<int:indice>', methods=['GET', 'POST'])
def editar_anuncio(indice):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    anuncios_lista = anuncios.carregar_anuncios()

    # Verifica se o índice é válido e se o anúncio pertence ao usuário logado
    if indice >= len(anuncios_lista) or anuncios_lista[indice].get('email') != session['usuario']:
        abort(403)  # Acesso negado

    anuncio = anuncios_lista[indice]

    if request.method == 'POST':
        anuncio['nome_produto'] = request.form['nome_produto']
        anuncio['anunciante'] = request.form['anunciante']
        anuncio['descricao'] = request.form['descricao']
        anuncio['link'] = request.form['link']

        imagem = request.files['imagem']
        if imagem and imagem.filename != '':
            nome_arquivo = secure_filename(imagem.filename)
            caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            imagem.save(caminho_imagem)
            anuncio['imagem'] = nome_arquivo

        anuncios.editar_anuncio(indice, anuncio)
        flash("Anúncio editado com sucesso!")
        return redirect(url_for('meus_anuncios'))

    return render_template('editar_anuncio.html', anuncio=anuncio, indice=indice)

@app.route('/excluir_anuncio/<int:indice>')
def excluir_anuncio(indice):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    lista = anuncios.carregar_anuncios()
    if indice >= len(lista) or lista[indice].get('email') != session['usuario']:
        abort(403)  # Acesso negado

    anuncios.excluir_anuncio(indice)
    flash("Anúncio excluído com sucesso!")
    return redirect(url_for('meus_anuncios'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
