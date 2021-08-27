import sqlite3

from flask import Flask, request, session
from flask import g # global
from flask import redirect # redirecionamento de página
from flask import abort # aborta requisição e retorna erro
from flask import render_template # renderiza um template
from flask import flash
from flask import url_for

# configuração
DATABASE = "blog.db"
SECRET_KEY = "pudim" # encripta e desencripta as informações

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/hello') # passa uma string que será a URL. Então liga a URL a uma função do python
def pagina_inicial():
    return "Hello World" # se o cliente requisitar '/hello' na página, o Flask executa a função pagina e retorna Hello World

@app.before_request
def antes_requisicao():
    g.bd = conectar_bd() # g é uma variável global no flask.


@app.teardown_request
def depois_request(exc):
    g.bd.close()

'''@app.route('/')
@app.route('/entradas') # uma segunda rota que leva para a mesma página
def exibir_entradas():
    sql = "select titulo, texto from entradas "

    return render_template('exibir_entradas.html', mensagem="Olá pessoas", img='https://img.olhardigital.com.br/wp-content/uploads/2021/02/shutterstock_1041249343-2000x450.jpg')
'''

@app.route('/')
@app.route('/entradas', methods=['POST']) # uma segunda rota que leva para a mesma página
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC" # script sql para pegar os dados e ordernar
    cur = g.bd.execute(sql) # executa o sql. Resultado no formato do banco
    entradas = [] # lista vazia
    for titulo, texto in cur.fetchall(): # fetchall traz os resultados
        entradas.append({'título': titulo, 'texto': texto}) # dicionário onde título e texto estarão guardados 
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?,?)"
    g.bd.execute(sql, request.form['campoTitulo'], request.form['campoTexto'])
    g.bd.commit()
    return redirect('/entradas')


@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('exibir_entradas'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['campoUsuario'] != 'admin' or request.form['campoSenha'] != 'admin':
            erro = 'senha ou usuário inválido'
        else:
            session['logado'] = True
            return redirect(url_for('exibir_entradas'))
    return render_template('login.html', erro='erro')