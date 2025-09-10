import api from './api';

export const getJobs = params => api.get('/jobs/applications/', { params });
export const getJob = id => api.get(`/jobs/applications/${id}/`);
export const createJob = data => api.post('/jobs/applications/', data);
export const updateJob = (id, data) => api.put(`/jobs/applications/${id}/`, data);
export const deleteJob = id => api.delete(`/jobs/applications/${id}/`);
export const getJobActivities = id => api.get(`/jobs/applications/${id}/activities/`);
export const getJobStats = () => api.get('/jobs/applications/statistics/');
export const getJobTimeline = () => api.get('/jobs/applications/timeline/'); 