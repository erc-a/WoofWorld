import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const Profile = () => {
  const { user, login: updateUserContext, loading: authLoading, token } = useContext(AuthContext); // Ganti nama login ke updateUserContext biar lebih jelas
  const navigate = useNavigate(); // Hook untuk navigasi

  const [formData, setFormData] = useState({
    name: '',
    email: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!authLoading && user) {
      setFormData({
        name: user.name || '',
        email: user.email || ''
      });
    } else if (!authLoading && !user) {
      // Jika user tidak ada setelah loading selesai, redirect ke login
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    if (!formData.name || !formData.email) {
      setError("Nama dan email tidak boleh kosong.");
      setLoading(false);
      return;
    }

    try {
      // Pastikan VITE_API_URL sudah benar di .env
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Kirim token untuk autentikasi
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email
        })
      });

      const data = await response.json();

      if (response.ok) {
        updateUserContext(data.user, token); // Update context dengan user baru
        setSuccess('Profil berhasil diperbarui!');
      } else {
        setError(data.message || 'Gagal memperbarui profil.');
      }
    } catch (err) {
      console.error('Error updating profile:', err);
      setError('Terjadi kesalahan saat memperbarui profil.');
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || (!user && !authLoading)) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-100px)]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="pt-28 pb-12 min-h-screen bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-lg mx-auto p-8 bg-white rounded-xl shadow-2xl">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Edit Profil</h2>

        {error && <div className="mb-4 p-3 text-sm text-red-700 bg-red-100 rounded-lg shadow-sm">{error}</div>}
        {success && <div className="mb-4 p-3 text-sm text-green-700 bg-green-100 rounded-lg shadow-sm">{success}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex flex-col items-center mb-8">
            <div className="w-28 h-28 rounded-full bg-blue-500 flex items-center justify-center text-white text-5xl font-semibold mb-4 shadow-md">
              {user?.name?.[0]?.toUpperCase() || '?'}
            </div>
          </div>

          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">Nama</label>
            <input
              type="text"
              name="name"
              id="name"
              value={formData.name}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              required
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="email"
              id="email"
              value={formData.email}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-3 px-4 rounded-lg font-semibold hover:opacity-90 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70"
          >
            {loading ? 'Menyimpan...' : 'Simpan Perubahan'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;