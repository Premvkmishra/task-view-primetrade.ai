const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:4000/api/v1';

async function request(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  const json = await res.json().catch(() => ({}));
  if (!res.ok || json?.success === false) {
    const msg = json?.message || res.statusText || 'Request failed';
    throw new Error(msg);
  }
  return json;
}

export const api = {
  post: <T>(path: string, body: unknown) => request(path, { method: 'POST', body: JSON.stringify(body) }) as Promise<T>,
  get: <T>(path: string) => request(path) as Promise<T>,
  put: <T>(path: string, body: unknown) => request(path, { method: 'PUT', body: JSON.stringify(body) }) as Promise<T>,
  delete: <T>(path: string) => request(path, { method: 'DELETE' }) as Promise<T>,
};

export { BASE_URL };
