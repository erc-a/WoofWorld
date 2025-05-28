import { createContext, useContext, useState, useEffect } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setTokenState] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  const handleLogout = () => {
    setUser(null);
    setTokenState(null);
    localStorage.removeItem('token');
  };

  const checkAuth = async (tokenToCheck) => {
    if (!tokenToCheck) {
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/verify-token`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${tokenToCheck}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        // Ensure token is still valid in localStorage
        if (!localStorage.getItem('token')) {
          localStorage.setItem('token', tokenToCheck);
        }
      } else {
        console.error('Token verification failed:', response.status);
        handleLogout();
      }
    } catch (error) {
      console.error('Auth check failed:', error.message);
      handleLogout();
    } finally {
      setLoading(false);
    }
  };

  // Add interval for periodic token verification
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setTokenState(storedToken);
      checkAuth(storedToken);
    } else {
      setLoading(false);
    }

    // Verify token every 5 minutes
    const interval = setInterval(() => {
      const currentToken = localStorage.getItem('token');
      if (currentToken) {
        checkAuth(currentToken);
      }
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const login = (userData, newToken) => {
    setUser(userData);
    setTokenState(newToken);
    localStorage.setItem('token', newToken);
  };

  const logout = () => {
    handleLogout();
  };

  const updateUser = (newUserData) => {
    setUser(newUserData);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      token, 
      loading, 
      login, 
      logout, 
      updateUser,
      checkAuth // Export checkAuth so it can be called manually if needed
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);