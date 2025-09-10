import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('pending');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link.');
      return;
    }
    axios.post('/api/users/verify-email/', { token })
      .then(() => {
        setStatus('success');
        setMessage('Email verified! You can now log in.');
        toast.success('Email verified!');
      })
      .catch(() => {
        setStatus('error');
        setMessage('Verification failed or link expired.');
        toast.error('Verification failed.');
      });
  }, [searchParams]);

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 mt-12 text-center">
      <h2 className="text-2xl font-bold text-primary-700 mb-6">Verify Email</h2>
      {status === 'pending' && <div className="text-slate-500">Verifying...</div>}
      {status === 'success' && (
        <>
          <div className="text-success-600 mb-4">{message}</div>
          <Link to="/login" className="text-primary-600 hover:underline">Go to Login</Link>
        </>
      )}
      {status === 'error' && (
        <>
          <div className="text-danger-600 mb-4">{message}</div>
          <Link to="/register" className="text-primary-600 hover:underline">Register</Link>
        </>
      )}
    </div>
  );
};

export default VerifyEmailPage; 