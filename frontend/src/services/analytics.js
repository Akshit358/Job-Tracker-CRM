import api from './api';

export const getSystemAnalytics = () => api.get('/analytics/system/dashboard/');
export const getUserAnalytics = () => api.get('/analytics/user/dashboard/'); 