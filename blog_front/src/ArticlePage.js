import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { authFetch, updateArticle, deleteArticle } from './api';

function ArticlePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const res = await authFetch(`/api/articles/${id}/`);
        if (!res.ok) {
          setError('Не удалось загрузить статью');
          return;
        }
        const data = await res.json();
        setArticle(data);
        setTitle(data.title);
        setText(data.text);
      } catch (e) {
        setError('Ошибка сети');
      }
    };
    load();
  }, [id]);

  const handleDelete = async () => {
    if (!window.confirm('Удалить эту статью?')) return;
    try {
      const res = await deleteArticle(id);
      if (res.status === 204 || res.status === 200) {
        navigate('/articles');
      } else if (res.status === 403) {
        setError('У вас нет прав на удаление этой статьи');
      } else {
        setError('Не удалось удалить статью');
      }
    } catch {
      setError('Ошибка сети при удалении');
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const res = await updateArticle(id, { title, text });
      if (res.ok) {
        const data = await res.json();
        setArticle(data);
        setIsEditing(false);
      } else if (res.status === 403) {
        setError('У вас нет прав на редактирование этой статьи');
      } else {
        setError('Не удалось сохранить изменения');
      }
    } catch {
      setError('Ошибка сети при сохранении');
    }
  };

  if (error) return <p className="error">{error}</p>;
  if (!article) return <p>Загрузка...</p>;

  return (
    <div className="article-page">
      <Link to="/articles">← Назад к списку</Link>

      {!isEditing ? (
        <>
        <p>Автор: {article.author}</p>
        <p>Создано: {new Date(article.created_date).toLocaleString()}</p>

        <h2>{article.title}</h2>
        <p>{article.text}</p>

          <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
            <button onClick={() => setIsEditing(true)}>Редактировать</button>
            <button
              onClick={handleDelete}
              style={{ background: '#dc2626', color: '#fff' }}
            >
              Удалить
            </button>
          </div>
        </>
      ) : (
        <form onSubmit={handleSave} className="article-form">
          <h1>Редактирование статьи</h1>

          <label>Заголовок</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Заголовок"
          />

          <label>Текст</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={8}
          />

          <div className="article-form__actions">
            <button type="submit" className="btn-primary">
              Сохранить
            </button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => setIsEditing(false)}
            >
              Отмена
            </button>
          </div>

          {error && <div className="article-form__error">{error}</div>}
        </form>
      )}

    </div>
  );
}

export default ArticlePage;
