import React, { useState } from 'react';
import * as jobsApi from '../services/jobs';
import toast from 'react-hot-toast';

const statusOptions = [
  { value: 'applied', label: 'Applied' },
  { value: 'interviewing', label: 'Interviewing' },
  { value: 'offer', label: 'Offer' },
  { value: 'rejected', label: 'Rejected' },
];

const JobFormModal = ({ job, onClose, onSaved }) => {
  const [form, setForm] = useState({
    company_name: job?.company_name || '',
    job_title: job?.job_title || '',
    application_date: job?.application_date ? new Date(job.application_date).toISOString().split('T')[0] : '',
    status: job?.status || 'applied',
    notes: job?.notes || '',
    resume_url: job?.resume_url || '',
    interview_date: job?.interview_date ? new Date(job.interview_date).toISOString().slice(0, 16) : '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      // Prepare data for submission
      const submitData = { ...form };
      
      // Handle empty interview_date
      if (!submitData.interview_date) {
        delete submitData.interview_date;
      }
      
      // Handle empty resume_url
      if (!submitData.resume_url) {
        delete submitData.resume_url;
      }
      
      if (job) {
        await jobsApi.updateJob(job.id, submitData);
        toast.success('Application updated!');
      } else {
        await jobsApi.createJob(submitData);
        toast.success('Application added!');
      }
      onSaved();
    } catch (err) {
      console.error('Job save error:', err);
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          'Failed to save. Please check your input.';
      setError(errorMessage);
      toast.error('Failed to save application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-lg p-6 relative animate-fadeIn">
        <button
          className="absolute top-3 right-3 text-slate-400 hover:text-primary-600 text-xl"
          onClick={onClose}
          aria-label="Close"
        >
          &times;
        </button>
        <h2 className="text-xl font-bold text-primary-700 mb-4 text-center">
          {job ? 'Edit Application' : 'Add Application'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Company Name</label>
            <input
              type="text"
              name="company_name"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.company_name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Job Title</label>
            <input
              type="text"
              name="job_title"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.job_title}
              onChange={handleChange}
              required
            />
          </div>
          <div className="flex gap-2">
            <div className="flex-1">
              <label className="block text-sm font-medium mb-1">Application Date</label>
              <input
                type="date"
                name="application_date"
                className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
                value={form.application_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="flex-1">
              <label className="block text-sm font-medium mb-1">Status</label>
              <select
                name="status"
                className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
                value={form.status}
                onChange={handleChange}
                required
              >
                {statusOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Resume URL</label>
            <input
              type="url"
              name="resume_url"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.resume_url}
              onChange={handleChange}
              placeholder="https://..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Interview Date (optional)</label>
            <input
              type="datetime-local"
              name="interview_date"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.interview_date}
              onChange={handleChange}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Notes</label>
            <textarea
              name="notes"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.notes}
              onChange={handleChange}
              rows={3}
              placeholder="Add any notes..."
            />
          </div>
          {error && <div className="text-danger-600 text-sm text-center">{error}</div>}
          <button
            type="submit"
            className="w-full bg-primary-600 text-white py-2 rounded font-semibold hover:bg-primary-700 transition disabled:opacity-60"
            disabled={loading}
          >
            {loading ? 'Saving...' : job ? 'Save Changes' : 'Add Application'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default JobFormModal; 