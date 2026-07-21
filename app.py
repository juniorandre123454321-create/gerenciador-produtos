from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import json
import os
import hashlib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_muito_segura_aqui'

ARQUIVO_PRODUTOS = 'produtos.json'
ARQUIVO_USUARIOS = 'usuarios.json'

# FUNCOES DE USUARIO
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# FUNCOES DE PRODUTO
def carregar_produtos():
    if os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_produtos(produtos):
    with open(ARQUIVO_PRODUTOS, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

# DECORADOR DE LOGIN
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login para acessar esta pagina.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# TEMPLATES
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: white;
            border-radius: 8px;
            padding: 40px;
            width: 380px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 30px;
            font-size: 24px;
            font-weight: 600;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            color: #4a4a4a;
            font-weight: 500;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            font-size: 14px;
            transition: 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #4a6cf7;
            box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
        }
        .btn {
            width: 100%;
            padding: 10px;
            background: #4a6cf7;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn:hover {
            background: #3a5cd9;
        }
        .links {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
        .links a {
            color: #4a6cf7;
            text-decoration: none;
        }
        .links a:hover {
            text-decoration: underline;
        }
        .alert {
            padding: 10px 14px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Acesso</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" required placeholder="seu@email.com">
            </div>
            <div class="form-group">
                <label>Senha</label>
                <input type="password" name="senha" required placeholder="******">
            </div>
            <button type="submit" class="btn">Entrar</button>
        </form>
        <div class="links">
            <p>Nao tem conta? <a href="{{ url_for('cadastro') }}">Cadastre-se</a></p>
        </div>
    </div>
</body>
</html>
"""

CADASTRO_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .cadastro-container {
            background: white;
            border-radius: 8px;
            padding: 40px;
            width: 420px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #1a1a1a;
            margin-bottom: 30px;
            font-size: 24px;
            font-weight: 600;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            color: #4a4a4a;
            font-weight: 500;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            font-size: 14px;
            transition: 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #4a6cf7;
            box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
        }
        .btn {
            width: 100%;
            padding: 10px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn:hover {
            background: #218838;
        }
        .links {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
        .links a {
            color: #4a6cf7;
            text-decoration: none;
        }
        .links a:hover {
            text-decoration: underline;
        }
        .alert {
            padding: 10px 14px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="cadastro-container">
        <h1>Criar Conta</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="form-group">
                <label>Nome Completo</label>
                <input type="text" name="nome" required placeholder="Seu nome">
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" required placeholder="seu@email.com">
            </div>
            <div class="form-group">
                <label>Senha</label>
                <input type="password" name="senha" required placeholder="Minimo 6 caracteres" minlength="6">
            </div>
            <button type="submit" class="btn">Cadastrar</button>
        </form>
        <div class="links">
            <p>Ja tem conta? <a href="{{ url_for('login') }}">Faça login</a></p>
        </div>
    </div>
</body>
</html>
"""

TEMPLATE_PRINCIPAL = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Produtos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .header h1 {
            color: #1a1a1a;
            font-size: 22px;
            font-weight: 600;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .user-info span {
            color: #4a4a4a;
            font-weight: 500;
            font-size: 14px;
        }
        .btn-sair {
            background: #dc3545;
            color: white;
            border: none;
            padding: 6px 18px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            transition: 0.2s;
        }
        .btn-sair:hover {
            background: #c82333;
        }
        .form-produto {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 25px;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 12px;
            align-items: end;
        }
        .form-produto input {
            padding: 8px 12px;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            font-size: 14px;
            transition: 0.2s;
        }
        .form-produto input:focus {
            outline: none;
            border-color: #4a6cf7;
            box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
        }
        .btn {
            padding: 8px 20px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover {
            opacity: 0.9;
        }
        .btn-primary {
            background: #4a6cf7;
            color: white;
        }
        .btn-editar {
            background: #17a2b8;
            color: white;
            padding: 4px 12px;
            font-size: 12px;
        }
        .btn-excluir {
            background: #dc3545;
            color: white;
            padding: 4px 12px;
            font-size: 12px;
        }
        .tabela-produtos {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 14px;
        }
        .tabela-produtos th {
            background: #f8f9fa;
            color: #1a1a1a;
            padding: 10px 12px;
            text-align: left;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 600;
        }
        .tabela-produtos td {
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        .tabela-produtos tr:hover {
            background: #f8f9fa;
        }
        .sem-produtos {
            text-align: center;
            padding: 30px;
            color: #999;
            font-size: 16px;
        }
        .alert {
            padding: 10px 14px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .acoes {
            display: flex;
            gap: 5px;
        }
        .total {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
            font-weight: 500;
            color: #1a1a1a;
            font-size: 14px;
        }
        @media (max-width: 768px) {
            .form-produto {
                grid-template-columns: 1fr;
            }
            .header {
                flex-direction: column;
                gap: 15px;
            }
            .tabela-produtos {
                font-size: 13px;
            }
            .acoes {
                flex-direction: column;
                gap: 3px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Gerenciador de Produtos</h1>
            <div class="user-info">
                <span>Olá, {{ session.nome_usuario }}</span>
                <a href="{{ url_for('logout') }}" class="btn-sair">Sair</a>
            </div>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST" class="form-produto">
            <input type="hidden" name="id_editar" value="{{ id_editar or '' }}">
            <input type="text" name="nome" placeholder="Nome do produto" value="{{ nome_editar or '' }}" required>
            <input type="number" name="preco" placeholder="Preco (R$)" step="0.01" value="{{ preco_editar or '' }}" required>
            <input type="number" name="quantidade" placeholder="Quantidade" value="{{ quantidade_editar or '' }}" required>
            <button type="submit" class="btn btn-primary">
                {% if id_editar %}Atualizar{% else %}Adicionar{% endif %}
            </button>
        </form>
        
        <table class="tabela-produtos">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Produto</th>
                    <th>Preco</th>
                    <th>Quantidade</th>
                    <th>Total</th>
                    <th>Acoes</th>
                </tr>
            </thead>
            <tbody>
                {% if produtos %}
                    {% for p in produtos %}
                    <tr>
                        <td>{{ p.id }}</td>
                        <td>{{ p.nome }}</td>
                        <td>R$ {{ "%.2f"|format(p.preco) }}</td>
                        <td>{{ p.quantidade }}</td>
                        <td>R$ {{ "%.2f"|format(p.preco * p.quantidade) }}</td>
                        <td>
                            <div class="acoes">
                                <a href="{{ url_for('editar', id=p.id) }}" class="btn btn-editar">Editar</a>
                                <a href="{{ url_for('excluir', id=p.id) }}" class="btn btn-excluir" onclick="return confirm('Tem certeza que deseja excluir este produto?')">Excluir</a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="6" class="sem-produtos">Nenhum produto cadastrado</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
        
        <div class="total">
            Total de produtos: {{ produtos|length }} | 
            Valor total em estoque: R$ {{ "%.2f"|format(total_geral) }}
        </div>
    </div>
</body>
</html>
"""

# ROTAS
@app.route('/')
def home():
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = hash_senha(request.form.get('senha'))
        
        usuarios = carregar_usuarios()
        usuario = next((u for u in usuarios if u['email'] == email and u['senha'] == senha), None)
        
        if usuario:
            session['usuario_id'] = usuario['id']
            session['nome_usuario'] = usuario['nome']
            session['email_usuario'] = usuario['email']
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = hash_senha(request.form.get('senha'))
        
        usuarios = carregar_usuarios()
        
        if any(u['email'] == email for u in usuarios):
            flash('Este email ja esta cadastrado.', 'danger')
            return render_template_string(CADASTRO_TEMPLATE)
        
        novo_id = max([u['id'] for u in usuarios], default=0) + 1
        usuarios.append({
            'id': novo_id,
            'nome': nome,
            'email': email,
            'senha': senha
        })
        salvar_usuarios(usuarios)
        
        flash('Cadastro realizado com sucesso. Faca login.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(CADASTRO_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash('Voce saiu do sistema.', 'success')
    return redirect(url_for('login'))

@app.route('/gerenciar', methods=['GET', 'POST'])
@login_obrigatorio
def index():
    produtos = carregar_produtos()
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        quantidade = int(request.form.get('quantidade'))
        id_editar = request.form.get('id_editar')
        
        if id_editar:
            for p in produtos:
                if str(p['id']) == id_editar:
                    p['nome'] = nome
                    p['preco'] = preco
                    p['quantidade'] = quantidade
                    break
            salvar_produtos(produtos)
            flash('Produto atualizado com sucesso.', 'success')
        else:
            novo_id = max([p['id'] for p in produtos], default=0) + 1
            produtos.append({
                'id': novo_id,
                'nome': nome,
                'preco': preco,
                'quantidade': quantidade
            })
            salvar_produtos(produtos)
            flash('Produto adicionado com sucesso.', 'success')
        
        return redirect(url_for('index'))
    
    total_geral = sum(p['preco'] * p['quantidade'] for p in produtos)
    
    return render_template_string(
        TEMPLATE_PRINCIPAL,
        produtos=produtos,
        total_geral=total_geral
    )

@app.route('/editar/<int:id>')
@login_obrigatorio
def editar(id):
    produtos = carregar_produtos()
    produto = next((p for p in produtos if p['id'] == id), None)
    
    if produto:
        return render_template_string(
            TEMPLATE_PRINCIPAL,
            produtos=produtos,
            id_editar=produto['id'],
            nome_editar=produto['nome'],
            preco_editar=produto['preco'],
            quantidade_editar=produto['quantidade'],
            total_geral=sum(p['preco'] * p['quantidade'] for p in produtos)
        )
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
@login_obrigatorio
def excluir(id):
    produtos = carregar_produtos()
    produtos = [p for p in produtos if p['id'] != id]
    salvar_produtos(produtos)
    flash('Produto excluido com sucesso.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
