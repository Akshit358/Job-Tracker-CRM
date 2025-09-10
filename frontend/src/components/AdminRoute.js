import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../services/AuthProvider';

const AdminRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  if (!user || user.role !== 'admin') {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default AdminRoute; 