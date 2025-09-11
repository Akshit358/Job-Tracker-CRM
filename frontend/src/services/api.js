import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
  withCredentials: true,
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  config => {
    // Don't add auth token for registration and login endpoints
    const authEndpoints = ['/users/register/', '/auth/login/', '/auth/token/', '/users/verify-email/'];
    const isAuthEndpoint = authEndpoints.some(endpoint => config.url?.includes(endpoint));
    
    if (!isAuthEndpoint) {
      const token = localStorage.getItem('access');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Optionally handle global logout or token refresh
    }
    return Promise.reject(error);
  }
);

export default api;
