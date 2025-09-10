import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const getInitialAuth = () => {
  const user = localStorage.getItem('user');
  const access = localStorage.getItem('access');
  const refresh = localStorage.getItem('refresh');
  return {
    user: user ? JSON.parse(user) : null,
    access,
    refresh,
  };
};

const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(getInitialAuth());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (auth.user && auth.access) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${auth.access}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [auth]);

  const login = (user, access, refresh) => {
    setAuth({ user, access, refresh });
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
  };

  const logout = () => {
    setAuth({ user: null, access: null, refresh: null });
    localStorage.removeItem('user');
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  };

  return (
    <AuthContext.Provider value={{ ...auth, login, logout, loading, setLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider; 