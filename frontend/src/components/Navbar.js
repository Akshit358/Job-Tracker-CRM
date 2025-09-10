import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../services/AuthProvider';
import clsx from 'clsx';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-sm py-3 px-4 flex items-center justify-between">
      <Link to="/" className="font-bold text-xl text-primary-700">Job Tracker CRM</Link>
      <div className="flex items-center gap-4">
        {!user && (
          <>
            <Link to="/login" className="text-primary-700 hover:underline">Login</Link>
            <Link to="/register" className="text-primary-700 hover:underline">Register</Link>
          </>
        )}
        {user && (
          <>
            <Link to="/dashboard" className="text-primary-700 hover:underline">Dashboard</Link>
            {user.role === 'admin' && (
              <Link to="/admin" className="text-primary-700 hover:underline">Admin</Link>
            )}
            <button
              onClick={handleLogout}
              className={clsx(
                'ml-2 px-3 py-1 rounded bg-primary-600 text-white hover:bg-primary-700 transition',
                'focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2'
              )}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 