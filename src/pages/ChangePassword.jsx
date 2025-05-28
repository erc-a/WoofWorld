import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

const ChangePassword = () => {
  const [email, setEmail] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      return setError('Password baru dan konfirmasi password tidak cocok');
    }

    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:6544/api/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          oldPassword,
          newPassword
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Password berhasil diubah');
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        setError(data.message || 'Gagal mengubah password');
      }
    } catch (error) {
      setError('Terjadi kesalahan. Silakan coba lagi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-20 pb-12 flex flex-col bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-md w-full mx-auto mt-8 bg-white p-8 border border-gray-200 rounded-2xl shadow-lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Ubah Password</h2>
            <p className="text-gray-600 mt-2">Masukkan data untuk mengubah password</p>
          </div>

          {error && (
            <div className="mb-4 p-4 text-sm text-red-700 bg-red-100 rounded-lg">
              {error}
            </div>
          )}

          {message && (
            <div className="mb-4 p-4 text-sm text-green-700 bg-green-100 rounded-lg">
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="text-sm font-medium text-gray-700 block mb-2">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label htmlFor="oldPassword" className="text-sm font-medium text-gray-700 block mb-2">
                Password Lama
              </label>
              <input
                type="password"
                id="oldPassword"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label htmlFor="newPassword" className="text-sm font-medium text-gray-700 block mb-2">
                Password Baru
              </label>
              <input
                type="password"
                id="newPassword"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="text-sm font-medium text-gray-700 block mb-2">
                Konfirmasi Password Baru
              </label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-3 px-4 rounded-lg hover:opacity-90 transition duration-300 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Ubah Password'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <a href="/login" className="text-sm text-blue-600 hover:underline">
              Kembali ke Login
            </a>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ChangePassword;