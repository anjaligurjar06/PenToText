const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function getToken() {
  return localStorage.getItem('ptt_token');
}

export function setSession(token, user) {
  localStorage.setItem('ptt_token', token);
  localStorage.setItem('ptt_user', JSON.stringify(user));
}

export function clearSession() {
  localStorage.removeItem('ptt_token');
  localStorage.removeItem('ptt_user');
}

export function getSessionUser() {
  const raw = localStorage.getItem('ptt_user');
  return raw ? JSON.parse(raw) : null;
}

async function request(path, { method = 'GET', body, isForm = false } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body && !isForm) headers['Content-Type'] = 'application/json';

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail || detail;
    } catch {
      // response had no JSON body
    }
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  register: (name, email, password) => request('/auth/register', { method: 'POST', body: { name, email, password } }),
  login: (email, password) => request('/auth/login', { method: 'POST', body: { email, password } }),
  me: () => request('/auth/me'),

  listDocuments: () => request('/documents'),
  getDocument: (id) => request(`/documents/${id}`),
  updateDocument: (id, payload) => request(`/documents/${id}`, { method: 'PATCH', body: payload }),
  deleteDocument: (id) => request(`/documents/${id}`, { method: 'DELETE' }),
  createDocument: (formData) => request('/documents', { method: 'POST', body: formData, isForm: true }),
};
