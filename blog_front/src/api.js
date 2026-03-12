const API_URL = 'http://127.0.0.1:8000';

export function getTokens() {
  return {
    access: localStorage.getItem('access') || '',
    refresh: localStorage.getItem('refresh') || '',
  };
}

export function saveTokens(access, refresh) {
  if (access) localStorage.setItem('access', access);
  if (refresh) localStorage.setItem('refresh', refresh);
}

export function clearTokens() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}

export async function authFetch(url, options = {}) {
  let { access, refresh } = getTokens();

  const baseOptions = {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: access ? `Bearer ${access}` : '',
      'Content-Type':
        options.body && !(options.headers && options.headers['Content-Type'])
          ? 'application/json'
          : options.headers && options.headers['Content-Type'],
    },
  };

  let res = await fetch(API_URL + url, baseOptions);

  if (res.status === 401 && refresh) {
    const refreshRes = await fetch(API_URL + '/api/token/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      access = data.access;
      saveTokens(access, null);

      const retryOptions = {
        ...baseOptions,
        headers: {
          ...(baseOptions.headers || {}),
          Authorization: `Bearer ${access}`,
        },
      };
      res = await fetch(API_URL + url, retryOptions);
    }
  }

  return res;
}

export async function createArticle(payload) {
  return authFetch('/api/articles/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateArticle(id, payload) {
  return authFetch(`/api/articles/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export async function deleteArticle(id) {
  const res = await authFetch(`/api/articles/${id}/`, {
    method: 'DELETE',
  });
  return res;
}