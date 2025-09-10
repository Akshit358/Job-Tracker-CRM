import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../services/AuthProvider';
import { register } from '../services/user';
import toast from 'react-hot-toast';

const RegisterPage = () => {
  const { setLoading, loading } = useContext(AuthContext);
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    password_confirm: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      await register(form);
      setSuccess('Registration successful! Please check your email to verify your account.');
      toast.success('Registration successful! Check your email.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      console.error('Registration error:', err.response?.data);
      setError(
        err.response?.data?.email?.[0] ||
        err.response?.data?.password?.[0] ||
        err.response?.data?.detail ||
        'Registration failed. Please try again.'
      );
      toast.error('Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 mt-12">
      <h2 className="text-2xl font-bold text-primary-700 mb-6 text-center">Create Account</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="flex gap-2">
          <div className="flex-1">
            <label className="block text-sm font-medium mb-1">First Name</label>
            <input
              type="text"
              name="first_name"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium mb-1">Last Name</label>
            <input
              type="text"
              name="last_name"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={form.last_name}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            name="email"
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password"
            name="password"
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Confirm Password</label>
          <input
            type="password"
            name="password_confirm"
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
            value={form.password_confirm}
            onChange={handleChange}
            required
          />
        </div>
        {error && <div className="text-danger-600 text-sm text-center">{error}</div>}
        {success && <div className="text-success-600 text-sm text-center">{success}</div>}
        <button
          type="submit"
          className="w-full bg-primary-600 text-white py-2 rounded font-semibold hover:bg-primary-700 transition disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <div className="flex justify-between mt-4 text-sm">
        <Link to="/login" className="text-primary-600 hover:underline">Already have an account?</Link>
      </div>
    </div>
  );
};

export default RegisterPage; 