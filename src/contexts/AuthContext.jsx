import { createContext, useContext, useState, useEffect } from 'react';

export const AuthContext = createContext(null);


export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token with backend
      checkAuth(token);
    } else {
      setLoading(false);
    }
  }, []);  const checkAuth = async (token) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/verify-token`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        console.error('Token verification failed:', response.status);
        localStorage.removeItem('token');
        setUser(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error.message);
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = (userData, token) => {
    setUser(userData);
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);