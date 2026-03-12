import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createArticle } from './api';

function CreateArticle() {
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const res = await createArticle({ title, text });
      if (res.ok) {
        const data = await res.json();
        navigate(`/articles/${data.id}`);
      } else {
        setError('Не удалось создать статью');
      }
    } catch {
      setError('Ошибка сети');
    }
  };

return (
  <div className="article-page">
    <Link to="/articles">← Назад к списку</Link>

    <form onSubmit={handleSubmit} className="article-form">
      <h1>Новая статья</h1>

      <label>Заголовок</label>
      <input
        type="text"
        placeholder="Заголовок"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <label>Текст</label>
      <textarea
        rows={8}
        placeholder="Текст статьи"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="article-form__actions">
        <button type="submit" className="btn-primary">
          Создать
        </button>
        <button
          type="button"
          className="btn-secondary"
          onClick={() => navigate(-1)}
        >
          Отмена
        </button>
      </div>

      {error && <div className="article-form__error">{error}</div>}
    </form>
  </div>
);

}

export default CreateArticle;
