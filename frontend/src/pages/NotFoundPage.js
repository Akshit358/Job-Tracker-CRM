import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
    <h1 className="text-6xl font-bold text-primary-700 mb-4">404</h1>
    <p className="text-lg text-slate-600 mb-6">Sorry, the page you are looking for does not exist.</p>
    <Link to="/" className="px-6 py-2 rounded bg-primary-600 text-white font-semibold hover:bg-primary-700 transition">Go Home</Link>
  </div>
);

export default NotFoundPage; 