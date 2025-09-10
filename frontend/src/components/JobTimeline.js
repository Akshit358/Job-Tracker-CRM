import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const JobTimeline = ({ timeline }) => {
  if (!timeline || timeline.length === 0) return null;
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-bold text-primary-700 mb-2 text-lg">Activity Timeline</h3>
      <ResponsiveContainer width="100%" height={120}>
        <BarChart data={timeline} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default JobTimeline; 