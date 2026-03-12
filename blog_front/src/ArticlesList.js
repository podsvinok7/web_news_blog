import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { authFetch } from './api';

function ArticlesList() {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const res = await authFetch('/api/articles/');
        if (!res.ok) {
          setError('Не удалось загрузить статьи');
          return;
        }
        const data = await res.json();
        setArticles(data);
      } catch (e) {
        setError('Ошибка сети');
      }
    };
    load();
  }, []);

  if (error) return <p className="error">{error}</p>;

  return (
    <div className="articles">
      <h2>Список статей</h2>
      {articles.map((a) => (
        <div key={a.id} className="article-card">
          <h3>
            <Link to={`/articles/${a.id}`}>{a.title}</Link>
          </h3>
          <p>{a.text?.slice(0, 150)}</p>
        </div>
      ))}
    </div>
  );
}

export default ArticlesList;
