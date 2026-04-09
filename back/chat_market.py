import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

from twilio.twiml.messaging_response import MessagingResponse

import google.genai as genai   # biblioteca nova

# Carregar variáveis de ambiente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# Criar cliente Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# for m in client.models.list():
#     print(m.name)

# Configuração do Flask
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

#---Banco SQLITE---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS listas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        produto TEXT) """)
    c.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT UNIQUE,
        preco NUMERIC,
        quantidade INT
        ) """)
    conn.commit()
    conn.close()
init_db()

#---Produtos Fictícios---
def popular_produtos():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    produtos_iniciais = [
        ("arroz", 5.99, 100),
        ("feijão", 7.99, 50),
        ("macarrão", 1.99, 200 ),
        ("leite", 4.59, 80),
        ("pão", 7.99, 60)
    ]
    for item, preco, qtd in produtos_iniciais:
        try:
            c.execute("INSERT INTO produtos (item, preco, quantidade) VALUES (?,?,?)", (item, preco, qtd))
        except sqlite3.IntegrityError:
            pass #já existe
    conn.commit()
    conn.close()    

# Função IA
def gerar_resposta_ia(mensagem:str)-> str:
    try:
        prompt_sistema = (
            "Você é um assistente de supermercado. "
            "Ajude o cliente com receitas e dúvidas sobre produtos. "
            "Responda em Português do Brasil de forma amigável."
        )
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",   
            contents=f"{prompt_sistema}\n\nCliente: {mensagem}"
        )
        return response.text if response.text else "Desculpe, não consegui processar sua pergunta."
    except Exception as e:
        print("Erro detalhado:", e)
        return "Estou com uma instabilidade técnica. Tente novamente em instantes."

#---ROTAS---
@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    user = c.fetchone()
    conn.close()
    if user:
        token = create_access_token(identity=usuario)
        return jsonify({"token": token})
    return jsonify({"Erro": "Usuário ou senha inválidos."}), 401

@app.route("/register", methods=["POST"])
def register():
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Usuário registrado com sucesso!"})
    except:
        return jsonify({"erro": "Usuário já existe"}), 400

@app.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    user_input = request.json.get("mensagem").lower()
    usuario = get_jwt_identity()
    resposta = processar_mensagem(user_input, usuario)
    return jsonify({"resposta": resposta})

# --- Comunicação com o whatsapp com twilio e flask
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    mensagem = request.values.get("Body", "").lower()
    usuario = request.values.get("From") #Número do usuário
    
    resposta_texto = processar_mensagem(mensagem, usuario)
    
    resp = MessagingResponse()
    resp.message(resposta_texto)
    
    return str(resp)

#---Processar mensagens---
def processar_mensagem(mensagem, usuario):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if "preço" in mensagem:
        c.execute("SELECT item, preco FROM produtos")
        for item, valor in c.fetchall():
            if item in mensagem:
                conn.close()
                return f"O preço do {item} é R$ {valor:.2f}"
        conn.close()
        return "Produto não encontrado."
    elif "lista" in mensagem:
        c.execute("SELECT produto FROM listas WHERE usuario=?", (usuario,))
        lista = [row[0] for row in c.fetchall()]
        conn.close()
        return f"Sua lista de compras: {', '.join(lista) if lista else 'vazia'}"
    elif "adicionar" in mensagem:
        c.execute("SELECT item FROM produtos")
        itens = [row[0] for row in c.fetchall()]
        for item in itens:
            if item in mensagem:
                c.execute("INSERT INTO listas (usuario, produto) VALUES (?, ?)", (usuario, item))
                conn.commit()
                conn.close()
                return f"{item} adicionado à sua lista."
        conn.close()
        return "Produto não encontrado para adicionar."
    elif "remover" in mensagem or "excluir" in mensagem:
        c.execute("SELECT id, produto FROM listas WHERE usuario=?", (usuario,))
        itens = c.fetchall()
        for item_id, produto in itens:
            if produto in mensagem:
                c.execute("DELETE FROM listas WHERE id=?", (item_id,))
                conn.commit()
                conn.close()
                return f"{produto} removido da sua lista."
        conn.close()
        return "Produto não encontrado para remover."
    elif  "limpar lista" in mensagem or "limpar" in mensagem:
        c.execute("DELETE FROM listas WHERE usuario=?", (usuario,))
        conn.commit()
        conn.close()
        return "Sua lista foi limpa."
    else:
        conn.close()
        return gerar_resposta_ia(mensagem)

init_db()
popular_produtos()

if __name__ == "__main__":
    app.run(debug=True)
