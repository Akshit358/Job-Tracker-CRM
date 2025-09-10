import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../services/AuthProvider';
import api from '../services/api';
import toast from 'react-hot-toast';

const LoginPage = () => {
  const { login, loading, setLoading } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/auth/login/', { email, password });
      login(res.data.user, res.data.access, res.data.refresh);
      toast.success('Welcome back!');
      navigate(res.data.user.role === 'admin' ? '/admin' : '/dashboard');
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Invalid credentials. Please try again.'
      );
      toast.error('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 mt-12">
      <h2 className="text-2xl font-bold text-primary-700 mb-6 text-center">Sign In</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password"
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <div className="text-danger-600 text-sm text-center">{error}</div>}
        <button
          type="submit"
          className="w-full bg-primary-600 text-white py-2 rounded font-semibold hover:bg-primary-700 transition disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
      <div className="flex justify-between mt-4 text-sm">
        <Link to="/reset-password" className="text-primary-600 hover:underline">Forgot password?</Link>
        <Link to="/register" className="text-primary-600 hover:underline">Create account</Link>
      </div>
    </div>
  );
};

export default LoginPage; 