from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importando o Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

# Inicializando o app e configurando o banco de dados
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o banco de dados com Flask-SQLAlchemy
db = SQLAlchemy(app)

# Configurando o Flask-Migrate para gerenciar migrações
migrate = Migrate(app, db)

# Modelo para a tabela de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # Aumentado para 255

@app.route('/')
def index():
    usuarios = Usuario.query.all()  # Consultar todos os usuários
    return render_template('index.html', usuarios=usuarios)  # Exibe a lista de usuários

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        # Hashing da senha com o método 'pbkdf2:sha256'
        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
        
        if nome and email and senha:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
            db.session.add(novo_usuario)
            db.session.commit()  # Salva no banco de dados
            return redirect(url_for('index'))  # Redireciona para a lista de usuários
    
    return render_template('criar.html')  # Exibe o formulário de criação

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)  # Busca o usuário pelo ID

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        senha = request.form['senha']
        
        # Atualiza a senha com hashing usando o método 'pbkdf2:sha256'
        usuario.senha = generate_password_hash(senha, method='pbkdf2:sha256')
        
        db.session.commit()  # Atualiza o banco de dados
        return redirect(url_for('index'))  # Redireciona de volta para a página inicial
    
    return render_template('editar.html', usuario=usuario)  # Exibe o formulário de edição

@app.route('/excluir/<int:id>')
def excluir(id):
    usuario = Usuario.query.get_or_404(id)  # Busca o usuário pelo ID
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))  # Redireciona para a lista de usuários

if __name__ == '__main__':
    app.run(debug=True)  # Rodando o servidor Flask
