import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch('http://localhost:6544/api/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Link reset password telah dikirim ke email Anda');
        setEmail('');
      } else {
        setError(data.message || 'Terjadi kesalahan');
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
            <div className="flex items-center justify-center mb-4">
              <img className="h-12 w-12" src="/public/fav_icon.svg" alt="WoofWorld Logo" />
              <span className="ml-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                WoofWorld
              </span>
            </div>
            <h2 className="text-3xl font-bold text-gray-900">Lupa Password</h2>
            <p className="text-gray-600 mt-2">Masukkan email Anda untuk reset password</p>
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
                placeholder="Masukkan email Anda"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-3 px-4 rounded-lg hover:opacity-90 transition duration-300 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Kirim Link Reset Password'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <Link 
              to="/login" 
              className="text-sm text-blue-600 hover:underline"
            >
              Kembali ke Login
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ForgotPassword;