import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
    <h1 className="text-4xl md:text-5xl font-bold mb-4 text-primary-700">Job Tracker CRM</h1>
    <p className="text-lg md:text-xl text-slate-600 mb-6 max-w-xl">
      Track your job applications, manage interviews, and stay organized with a modern, secure, and analytics-powered CRM for your job search journey.
    </p>
    <div className="flex gap-4">
      <Link to="/register" className="px-6 py-2 rounded bg-primary-600 text-white font-semibold hover:bg-primary-700 transition">Get Started</Link>
      <Link to="/login" className="px-6 py-2 rounded border border-primary-600 text-primary-700 font-semibold hover:bg-primary-50 transition">Login</Link>
    </div>
    <div className="mt-10 text-slate-400 text-xs">
      <span>Demo: admin@jobtracker.com / test123456</span>
    </div>
  </div>
);

export default HomePage; 