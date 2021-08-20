import sqlite3

from flask import Flask, request, session
from flask import g # global
from flask import redirect # redirecionamento de página
from flask import abort # aborta requisição e retorna erro
from flask import render_template # renderiza um template
from flask import flash

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

@app.route('/')
@app.route('/entradas') # uma segunda rota que leva para a mesma página
def exibir_entradas():
    return render_template('exibir_entradas.html')