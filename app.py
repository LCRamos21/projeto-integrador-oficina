from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Substitua por uma chave forte

# -----------------------
# Funções de Banco de Dados
# -----------------------

def init_ordens_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ordens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            modelo TEXT NOT NULL,
            problema TEXT NOT NULL,
            data_entrada TEXT NOT NULL,
            status TEXT NOT NULL,
            valor REAL
        )
    ''')
    conn.commit()
    conn.close()

def init_users_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_ordens_db()
init_users_db()

# -----------------------
# Rotas para Autenticação e Cadastro (sem alterações)
# -----------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('register'))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            flash('Usuário já existe.', 'warning')
            conn.close()
            return redirect(url_for('register'))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        flash('Usuário registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

# -----------------------
# Rotas para Ordens de Serviço (acesso restrito)
# -----------------------

# Página principal com Filtro e Pesquisa Avançada
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Recupera parâmetros de filtro da query string
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query = "SELECT * FROM ordens WHERE 1=1"
    params = []

    # Filtra por cliente (pesquisa parcial)
    if search:
        query += " AND cliente LIKE ?"
        params.append(f"%{search}%")
    
    # Filtra por status, se selecionado
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"
    c.execute(query, params)
    ordens = c.fetchall()
    conn.close()
    
    return render_template('index.html', ordens=ordens, search=search, status_filter=status_filter)

# Adiciona nova ordem
@app.route('/add', methods=['POST'])
def add_ordem():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cliente = request.form['cliente']
    modelo = request.form['modelo']
    problema = request.form['problema']
    data_entrada = request.form['data_entrada']
    status = request.form['status']
    valor = request.form.get('valor', 0)
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO ordens (cliente, modelo, problema, data_entrada, status, valor)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (cliente, modelo, problema, data_entrada, status, valor))
    conn.commit()
    conn.close()
    
    flash('Ordem cadastrada com sucesso!', 'success')
    return redirect(url_for('index'))

# Remoção de ordem
@app.route('/delete/<int:id>', methods=['POST'])
def delete_ordem(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM ordens WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Ordem removida com sucesso!', 'info')
    return redirect(url_for('index'))

# Edição de ordem – Exibe formulário com dados da ordem
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ordem(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        cliente = request.form['cliente']
        modelo = request.form['modelo']
        problema = request.form['problema']
        data_entrada = request.form['data_entrada']
        status = request.form['status']
        valor = request.form.get('valor', 0)
        
        c.execute('''
            UPDATE ordens
            SET cliente = ?, modelo = ?, problema = ?, data_entrada = ?, status = ?, valor = ?
            WHERE id = ?
        ''', (cliente, modelo, problema, data_entrada, status, valor, id))
        conn.commit()
        conn.close()
        
        flash('Ordem atualizada com sucesso!', 'success')
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM ordens WHERE id = ?", (id,))
        ordem = c.fetchone()
        conn.close()
        if ordem:
            return render_template('edit.html', ordem=ordem)
        else:
            flash('Ordem não encontrada.', 'warning')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
