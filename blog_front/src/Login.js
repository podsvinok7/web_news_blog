import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { saveTokens } from './api';

const API_URL = 'http://127.0.0.1:8000';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch(`${API_URL}/api/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError('Неверный логин или пароль');
        return;
      }

      const data = await res.json();
      saveTokens(data.access, data.refresh);
      navigate('/articles');
    } catch (err) {
      setError('Ошибка сети');
    }
  };

  return (
    <div className="login">
      <h2>Вход</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Войти</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Login;
