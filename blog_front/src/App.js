import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import './App.css';
import Login from './Login';
import ArticlesList from './ArticlesList';
import ArticlePage from './ArticlePage';
import CreateArticle from './CreateArticle';
import { getTokens, clearTokens } from './api';


function PrivateRoute({ children }) {
  const { access } = getTokens();
  if (!access) return <Navigate to="/Login" replace />;
  return children;
}

function App() {
  const handleLogout = () => {
    clearTokens();
    window.location.href = '/Login';
  };

  return (
    <Router>
      <div className="App">
        <header className="header">
          <h1><Link to="/articles">Новости</Link></h1>
          <nav>
            <Link to="/articles">Все статьи</Link>
            <Link to="/articles/new">Новая статья</Link>
            <button onClick={handleLogout}>Выйти</button>
          </nav>
        </header>


        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/articles"
            element={
              <PrivateRoute>
                <ArticlesList />
              </PrivateRoute>
            }
          />

          <Route
            path="/articles/new"
            element={
              <PrivateRoute>
                <CreateArticle />
              </PrivateRoute>
            }
          />

          <Route
            path="/articles/:id"
            element={
              <PrivateRoute>
                <ArticlePage />
              </PrivateRoute>
            }
          />

          <Route path="*" element={<Navigate to="/articles" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
