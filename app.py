
from flask import Flask, render_template, request, redirect, url_for, session
import yagmail
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email == 'admin' and senha == '123':
            session['usuario'] = email
            return redirect(url_for('dashboard'))
        else:
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
  
from flask import Flask, render_template, request, redirect, url_for, session
import yagmail
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if email == 'admin' and senha == '123':
            session['usuario'] = email
            return redirect(url_for('dashboard'))
        else:
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

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)