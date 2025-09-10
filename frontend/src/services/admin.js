import api from './api';

export const getUsers = params => api.get('/admin/users/', { params });
export const getUser = id => api.get(`/admin/users/${id}/`);
export const deactivateUser = id => api.post(`/admin/users/${id}/deactivate/`);
export const activateUser = id => api.post(`/admin/users/${id}/activate/`);
export const deleteUser = id => api.delete(`/admin/users/${id}/delete/`);
export const broadcast = data => api.post('/admin/broadcast/', data);
export const getAdminStats = () => api.get('/admin/dashboard/'); 