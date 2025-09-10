import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const statusColors = {
  applied: '#3b82f6',
  interviewing: '#f59e0b',
  offer: '#22c55e',
  rejected: '#ef4444',
};

const JobStats = ({ stats }) => {
  if (!stats) return null;
  const statusData = stats.status_distribution || [];
  const companyData = stats.top_companies || [];

  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-bold text-primary-700 mb-2 text-lg">Analytics</h3>
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span>Total Applications</span>
          <span className="font-semibold">{stats.total_applications}</span>
        </div>
        <div className="flex justify-between text-sm mb-2">
          <span>This Month</span>
          <span className="font-semibold">{stats.applications_this_month}</span>
        </div>
        <div className="flex justify-between text-sm mb-2">
          <span>This Week</span>
          <span className="font-semibold">{stats.applications_this_week}</span>
        </div>
      </div>
      <div className="mb-4">
        <h4 className="font-semibold text-sm mb-1">Status Distribution</h4>
        <ResponsiveContainer width="100%" height={120}>
          <PieChart>
            <Pie
              data={statusData}
              dataKey="count"
              nameKey="status"
              cx="50%"
              cy="50%"
              outerRadius={40}
              label={({ status }) => status.charAt(0).toUpperCase() + status.slice(1)}
            >
              {statusData.map((entry, idx) => (
                <Cell key={entry.status} fill={statusColors[entry.status] || '#64748b'} />
              ))}
            </Pie>
            <Legend verticalAlign="bottom" height={24} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div>
        <h4 className="font-semibold text-sm mb-1">Top Companies</h4>
        <ResponsiveContainer width="100%" height={120}>
          <BarChart data={companyData} layout="vertical">
            <XAxis type="number" hide />
            <YAxis dataKey="company_name" type="category" width={80} />
            <Bar dataKey="count" fill="#3b82f6" />
            <Tooltip />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default JobStats; 