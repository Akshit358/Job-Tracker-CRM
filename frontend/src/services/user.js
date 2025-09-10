import api from './api';

export const register = data => api.post('/users/register/', data);
export const getProfile = () => api.get('/users/profile/');
export const updateProfile = data => api.put('/users/update/', data);
export const changePassword = data => api.post('/users/change-password/', data); 