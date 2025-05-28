import { createContext, useContext, useState, useEffect } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setTokenState] = useState(localStorage.getItem('token')); // State untuk token
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setTokenState(storedToken); // Set token dari localStorage
      checkAuth(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const checkAuth = async (tokenToCheck) => {
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/verify-token`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${tokenToCheck}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData); // userData dari verify-token biasanya hanya data user
      } else {
        console.error('Token verification failed:', response.status);
        localStorage.removeItem('token');
        setUser(null);
        setTokenState(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error.message);
      localStorage.removeItem('token');
      setUser(null);
      setTokenState(null);
    } finally {
      setLoading(false);
    }
  };

  const login = (userData, newToken) => {
    setUser(userData);
    localStorage.setItem('token', newToken);
    setTokenState(newToken); // Update state token
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    setTokenState(null); // Reset state token
  };

  // Fungsi untuk mengupdate user data saja tanpa mengubah token, jika diperlukan
  // Atau bisa juga `login` diartikan sebagai "set sesi aktif"
  const updateUser = (newUserData) => {
    setUser(newUserData);
    // Tidak perlu update token di sini jika token tidak berubah
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);