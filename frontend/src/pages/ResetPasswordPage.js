import React, { useState } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const [step, setStep] = useState(searchParams.get('token') ? 2 : 1);
  const [email, setEmail] = useState('');
  const [token, setToken] = useState(searchParams.get('token') || '');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleRequest = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await axios.post('/api/users/reset-password/', { email });
      setSuccess('Password reset email sent! Check your inbox.');
      toast.success('Reset email sent!');
    } catch (err) {
      setError('Failed to send reset email.');
      toast.error('Failed to send reset email.');
    }
  };

  const handleConfirm = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (password !== passwordConfirm) {
      setError('Passwords do not match.');
      return;
    }
    try {
      await axios.post('/api/users/reset-password/confirm/', { token, new_password: password, new_password_confirm: passwordConfirm });
      setSuccess('Password reset! You can now log in.');
      toast.success('Password reset!');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError('Failed to reset password.');
      toast.error('Failed to reset password.');
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 mt-12 text-center">
      <h2 className="text-2xl font-bold text-primary-700 mb-6">Reset Password</h2>
      {step === 1 && (
        <form onSubmit={handleRequest} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          {error && <div className="text-danger-600 text-sm text-center">{error}</div>}
          {success && <div className="text-success-600 text-sm text-center">{success}</div>}
          <button type="submit" className="w-full bg-primary-600 text-white py-2 rounded font-semibold hover:bg-primary-700 transition">Send Reset Email</button>
        </form>
      )}
      {step === 2 && (
        <form onSubmit={handleConfirm} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-1">New Password</label>
            <input
              type="password"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Confirm New Password</label>
            <input
              type="password"
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-400"
              value={passwordConfirm}
              onChange={e => setPasswordConfirm(e.target.value)}
              required
            />
          </div>
          {error && <div className="text-danger-600 text-sm text-center">{error}</div>}
          {success && <div className="text-success-600 text-sm text-center">{success}</div>}
          <button type="submit" className="w-full bg-primary-600 text-white py-2 rounded font-semibold hover:bg-primary-700 transition">Reset Password</button>
        </form>
      )}
      <div className="mt-4 text-sm">
        <Link to="/login" className="text-primary-600 hover:underline">Back to Login</Link>
      </div>
    </div>
  );
};

export default ResetPasswordPage; 