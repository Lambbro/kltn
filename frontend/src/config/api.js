import axios from 'axios';

const api = axios.create({
 // baseURL: 'http://lamb.servebeer.com:8000',
  baseURL: 'http://192.168.10.142:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    console.log('Gửi token:', token); // Debug token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Lỗi response:', error.response?.status, error.response?.data);
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;