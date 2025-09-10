import React, { useEffect, useState } from 'react';
import * as jobsApi from '../services/jobs';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { Plus, Filter, BarChart2 } from 'lucide-react';
import JobFormModal from '../components/JobFormModal';
import JobTimeline from '../components/JobTimeline';
import JobStats from '../components/JobStats';

const statusColors = {
  applied: 'bg-blue-100 text-blue-700',
  interviewing: 'bg-yellow-100 text-yellow-700',
  offer: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
};

const DashboardPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editJob, setEditJob] = useState(null);
  const [filters, setFilters] = useState({ status: [], company: '' });
  const [stats, setStats] = useState(null);
  const [timeline, setTimeline] = useState([]);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const res = await jobsApi.getJobs({
        status: filters.status,
        company_name: filters.company,
      });
      console.log('Jobs API response:', res.data);
      const jobsData = res.data.results || res.data || [];
      console.log('Processed jobs data:', jobsData);
      setJobs(jobsData);
    } catch (err) {
      console.error('Failed to load jobs:', err);
      toast.error('Failed to load jobs');
      setJobs([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await jobsApi.getJobStats();
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load stats:', err);
      setStats(null);
    }
  };

  const fetchTimeline = async () => {
    try {
      const res = await jobsApi.getJobTimeline();
      setTimeline(res.data.timeline || res.data || []);
    } catch (err) {
      console.error('Failed to load timeline:', err);
      setTimeline([]);
    }
  };

  useEffect(() => {
    fetchJobs();
    fetchStats();
    fetchTimeline();
    // eslint-disable-next-line
  }, [filters]);

  // Ensure jobs is always an array
  const safeJobs = Array.isArray(jobs) ? jobs : [];

  const handleAdd = () => {
    setEditJob(null);
    setShowModal(true);
  };

  const handleEdit = job => {
    setEditJob(job);
    setShowModal(true);
  };

  const handleDelete = async id => {
    if (!window.confirm('Delete this job application?')) return;
    try {
      await jobsApi.deleteJob(id);
      toast.success('Deleted');
      fetchJobs();
      fetchStats();
      fetchTimeline();
    } catch {
      toast.error('Failed to delete');
    }
  };

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <h1 className="text-2xl font-bold text-primary-700">My Job Applications</h1>
        <div className="flex gap-2">
          <button
            onClick={handleAdd}
            className="flex items-center gap-2 px-4 py-2 rounded bg-primary-600 text-white font-semibold hover:bg-primary-700 transition"
          >
            <Plus size={18} /> Add Application
          </button>
        </div>
      </div>
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <div className="flex-1">
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              placeholder="Filter by company..."
              className="border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={filters.company}
              onChange={e => setFilters(f => ({ ...f, company: e.target.value }))}
            />
            <select
              className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={filters.status}
              onChange={e => setFilters(f => ({ ...f, status: e.target.value ? [e.target.value] : [] }))}
            >
              <option value="">All Statuses</option>
              <option value="applied">Applied</option>
              <option value="interviewing">Interviewing</option>
              <option value="offer">Offer</option>
              <option value="rejected">Rejected</option>
            </select>
            <button
              className="flex items-center gap-1 px-3 py-2 rounded bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200"
              onClick={() => setFilters({ status: [], company: '' })}
            >
              <Filter size={16} /> Reset
            </button>
          </div>
          <div className="overflow-x-auto rounded shadow bg-white">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="bg-slate-50">
                  <th className="py-2 px-3 text-left">Company</th>
                  <th className="py-2 px-3 text-left">Title</th>
                  <th className="py-2 px-3 text-left">Date</th>
                  <th className="py-2 px-3 text-left">Status</th>
                  <th className="py-2 px-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan={5} className="text-center py-8">Loading...</td></tr>
                ) : safeJobs.length === 0 ? (
                  <tr><td colSpan={5} className="text-center py-8 text-slate-400">No applications found.</td></tr>
                ) : safeJobs.map(job => (
                  <tr key={job.id} className="border-b hover:bg-slate-50">
                    <td className="py-2 px-3 font-medium">{job.company_name}</td>
                    <td className="py-2 px-3">{job.job_title}</td>
                    <td className="py-2 px-3">{format(new Date(job.application_date), 'MMM d, yyyy')}</td>
                    <td className="py-2 px-3">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${statusColors[job.status] || 'bg-slate-100 text-slate-700'}`}>{job.status_display}</span>
                    </td>
                    <td className="py-2 px-3 flex gap-2">
                      <button
                        className="text-primary-600 hover:underline"
                        onClick={() => handleEdit(job)}
                      >Edit</button>
                      <button
                        className="text-danger-600 hover:underline"
                        onClick={() => handleDelete(job.id)}
                      >Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="w-full md:w-80 flex flex-col gap-6">
          <JobStats stats={stats} />
          <JobTimeline timeline={timeline} />
        </div>
      </div>
      {showModal && (
        <JobFormModal
          job={editJob}
          onClose={() => setShowModal(false)}
          onSaved={() => {
            setShowModal(false);
            fetchJobs();
            fetchStats();
            fetchTimeline();
          }}
        />
      )}
    </div>
  );
};

export default DashboardPage; 