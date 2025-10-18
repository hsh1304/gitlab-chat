import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [useLLM, setUseLLM] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    const userMsg = { role: "user", text: message };
    setChat((c) => [...c, userMsg]);
    setMessage("");
    setLoading(true);
    try {
      const resp = await axios.post(
        "http://localhost:8000/chat",
        {
          message,
          use_llm: useLLM,
          llm_provider: useLLM ? "openai" : "none"
        },
        { timeout: 60000 }
      );
      setChat((c) => [...c, { role: "assistant", text: resp.data.answer }]);
    } catch (err) {
      setChat((c) => [...c, { role: "assistant", text: "Error: " + (err.response?.data?.detail || err.message) }]);
    } finally {
      setLoading(false);
    }
  };

  const onKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>GenAI Chatbot (Local)</h1>
        <label className="llm-toggle">
          <input type="checkbox" checked={useLLM} onChange={() => setUseLLM(!useLLM)} />
          Use hosted LLM (requires keys in backend .env)
        </label>
      </header>

      <div className="chat-window">
        {chat.map((m, i) => (
          <div key={i} className={m.role === "user" ? "bubble user" : "bubble assistant"}>
            {m.text}
          </div>
        ))}

        {loading && <div className="bubble assistant">Thinking…</div>}
      </div>

      <div className="composer">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={onKey}
          placeholder="Ask a question about the project brief or handbook..."
        />
        <button onClick={sendMessage} disabled={!message.trim() || loading}>
          Send
        </button>
      </div>
    </div>
  );
}
