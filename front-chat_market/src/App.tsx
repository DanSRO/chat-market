import './App.css';
import React, { useState } from "react";
import axios from "axios";
const API_URL = "http://localhost:5000";

function App() {
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [token, setToken] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [respostas, setRespostas] = useState<string[]>([]);

  const login = async () => {
    try {
      const resp = await axios.post(`${API_URL}/login`, { usuario, senha });
      setToken(resp.data.token);
      alert("Login realizado com sucesso.");
    } catch {
      alert("Erro no login.");
    }
  };

  const register = async () => {
    try {
      await axios.post(`${API_URL}/register`, { usuario, senha });
      alert("Usuário cadastrado com sucesso.");
      setIsRegister(false); // volta para login
    } catch {
      alert("Erro ao cadastrar usuário.");
    }
  };

  const enviarMensagem = async () => {
    if (!mensagem.trim()) return;
    if (!token) {
      alert("Faça login primeiro!");
      return;
    }
    try {
      const resp = await axios.post(
        `${API_URL}/chat`,
        { mensagem },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setRespostas([...respostas, `Você: ${mensagem}`, `Chat-Market: ${resp.data.resposta}`]);
      setMensagem("");
    } catch {
      alert("Erro ao enviar mensagens.");
    }
  };

  const logout = () => {
    setToken("");
    setUsuario("");
    setSenha("");
    setRespostas([]);
  }

  return (
    <div className='background-container'>
      <div className='container'>
        <h1>Chatbot Supermercado</h1>

        {/* Se não tiver token, mostra login/registro */}
        {!token ? (
          isRegister ? (
            <form onSubmit={(e)=> {e.preventDefault(); register();}}>
              <h2>Registrar</h2>
              <input
                placeholder="Usuário"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
              />
              <input
                type="password"
                placeholder="Senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
              />
              <button type="submit">Registrar</button>
              <p>
                Já tem conta?{" "}
                <button onClick={() => setIsRegister(false)}>Ir para o Login</button>
              </p>
            </form>
          ) : (
            <form onSubmit={(e)=> {e.preventDefault(); login();}}>
              <h2>Login</h2>
              <input
                placeholder="Usuário"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
              />
              <input
                type="password"
                placeholder="Senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
              />
              <button type="submit">Login</button>
              <p>
                Não tem conta?{" "}
                <button onClick={() => setIsRegister(true)}>Registrar</button>
              </p>
            </form>
          )
        ) : (
          // Se tiver token, mostra apenas o chat
          <form onSubmit={(e)=>{e.preventDefault(); enviarMensagem();}}>
            <div style={{ marginTop: "1rem" }}>
              <input
                placeholder="Digite sua mensagem..."
                value={mensagem}
                onChange={(e) => setMensagem(e.target.value)}
              />
              <button type='submit'>Enviar</button>
            </div>

            <div style={{ marginTop: "2rem" }}>
              <h2>Conversa</h2>
              <div className="chat-box">
                {respostas.map((r, i) => (
                  <p key={i} className={r.startsWith("Você:") ? "message-user" : "message-bot"}>{r}</p>
                ))}
              </div>
            </div>
          </form>
        )}
        {token && (
          <button 
            style={{position:"absolute", top:"10px", right:"10px"}}
            onClick={logout}
          >Logout</button>
        )}
      </div>
    </div>
  );
}

export default App;
