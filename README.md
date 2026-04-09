# 🛒 Chat Market - Chatbot de Supermercado

Projeto fullstack com **Flask (Python)** no backend e **React (TypeScript)** no frontend, integrado com **IA (Gemini)** e opcionalmente com **WhatsApp via Twilio**.

---

## 🚀 Funcionalidades

- Consulta de preços de produtos
- Criação e gerenciamento de lista de compras
- Chat com IA para dúvidas e receitas
- Integração com WhatsApp (via Twilio)
- Autenticação com JWT (frontend)

---

## 🧠 Tecnologias utilizadas

### Backend
- Python
- Flask
- SQLite
- JWT (flask-jwt-extended)
- Gemini API
- Twilio (WhatsApp)
- Ngrok (túnel para webhook)

### Frontend
- React
- TypeScript
- Axios

---

## 🚀 Como rodar o projeto

---

### 🔹 1. Clonar os repositórios

```bash
# Backend
git clone https://github.com/DanSRO/chat-market.git

# Frontend
git clone https://github.com/DanSRO/front-chat_market.git

Use no terminal para entrar no diretório do projeto
cd chat-market

Crie um arquivo .env com as variáveis como estão no .env.example
com as chaves da sua api e uma chave secreta para token

GEMINI_API_KEY=sua_chave_gemini_aqui
JWT_SECRET=umsegredoseguro

Instalar dependências
pip install -r requirements.txt

Para rodar o backend use :
python chat_market.py

No frontend instale as dependencias do npm 

entre no diretório 
cd frontend-chat_market

e use npm install

depois npm start para rodar

Servidor estará disponível em:
front em:
http://localhost:3000
e back em:
http://localhost:5000

📱 Integração com WhatsApp (Twilio)
🔹 Pré-requisitos
Conta no Twilio
Acesso ao WhatsApp Sandbox
Ngrok instalado

🔹 1. Rodar o ngrok

Em outro terminal:

ngrok http 5000

Você verá algo como:

https://abc123.ngrok-free.app

🔹 2. Configurar no Twilio

No painel do Twilio (WhatsApp Sandbox):

Campo:

WHEN A MESSAGE COMES IN

Coloque:

https://SEU_LINK_NGROK/whatsapp

Exemplo:

https://abc123.ngrok-free.app/whatsapp

🔹 3. Testar

Envie mensagem no WhatsApp:

preço do arroz

🔄 Fluxo da aplicação
Frontend (React)
        ↓
Backend Flask (/chat)
        ↓
SQLite + Gemini

OU

WhatsApp
        ↓
Twilio
        ↓
Ngrok
        ↓
Flask (/whatsapp)
        ↓
SQLite + Gemini


📦 Dependências
Backend (requirements.txt)
flask
flask-jwt-extended
flask-cors
python-dotenv
google-genai
twilio
Frontend (package.json)
react
axios
typescript


outras dependências listadas no projeto

🔐 Observações de segurança
Este projeto é para fins educacionais
Senhas estão armazenadas sem hash (não recomendado para produção)
Dados trafegam por serviços externos (Twilio, Ngrok, Gemini)
Não utilize dados sensíveis

⚠️ Limitações
URL do Ngrok muda a cada execução (plano gratuito)
Twilio Sandbox possui limitações de uso
SQLite não é ideal para produção

🚀 Melhorias futuras
Hash de senha
Banco de dados robusto (PostgreSQL)
Deploy em ambiente cloud
Autenticação no WhatsApp
Validação de requisições do Twilio

🤖 IA utilizada
Google Gemini API

Crie uma chave em:
https://ai.google.dev/

👨‍💻 Autor

Daniel Dantas