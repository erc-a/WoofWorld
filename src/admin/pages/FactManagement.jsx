// src/admin/pages/FactManagement.jsx
import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext'; // Lebih baik gunakan hook jika tersedia

const FactManagement = () => {
  const { token } = useAuth(); // Mengambil token dari AuthContext
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false); // Untuk loading saat submit form
  const [newFactContent, setNewFactContent] = useState('');
  const [editingFact, setEditingFact] = useState(null); // Objek fact yang sedang diedit
  const [editContent, setEditContent] = useState('');
  const [error, setError] = useState('');

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  const fetchFacts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      if (!token) {
        setError("Token tidak ditemukan. Silakan login ulang.");
        setLoading(false);
        return;
      }
      const response = await fetch(`${API_BASE_URL}/api/admin/facts`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Gagal mengambil daftar fakta' }));
        throw new Error(errorData.message);
      }
      const data = await response.json();
      setFacts(Array.isArray(data.facts) ? data.facts : []); // Pastikan data.facts adalah array
    } catch (err) {
      console.error('Error fetching facts:', err);
      setError(err.message || 'Gagal memuat fakta. Silakan coba lagi.');
      setFacts([]);
    } finally {
      setLoading(false);
    }
  }, [token, API_BASE_URL]);

  useEffect(() => {
    fetchFacts();
  }, [fetchFacts]);

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    if (!newFactContent.trim()) {
      setError('Konten fakta tidak boleh kosong.');
      return;
    }
    setIsSubmitting(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/facts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ content: newFactContent }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Gagal menambahkan fakta' }));
        throw new Error(errorData.message);
      }
      const addedFact = await response.json();
      setFacts(prevFacts => [addedFact, ...prevFacts.sort((a, b) => b.id - a.id)]); // Tambah di awal dan sort by ID desc
      setNewFactContent('');
    } catch (err) {
      console.error('Error adding fact:', err);
      setError(err.message || 'Gagal menambahkan fakta. Silakan coba lagi.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    if (!editingFact || !editContent.trim()) {
      setError('Konten fakta tidak boleh kosong.');
      return;
    }
    setIsSubmitting(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/facts/${editingFact.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ content: editContent }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Gagal memperbarui fakta' }));
        throw new Error(errorData.message);
      }
      const updatedFact = await response.json();
      setFacts(prevFacts =>
        prevFacts.map(fact => (fact.id === updatedFact.id ? updatedFact : fact))
      );
      setEditingFact(null);
      setEditContent('');
    } catch (err) {
      console.error('Error updating fact:', err);
      setError(err.message || 'Gagal memperbarui fakta. Silakan coba lagi.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (factId) => {
    if (!confirm('Apakah Anda yakin ingin menghapus fakta ini?')) return;
    // Optimistic UI update atau loading state bisa ditambahkan di sini
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/facts/${factId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Gagal menghapus fakta' }));
        throw new Error(errorData.message);
      }
      setFacts(prevFacts => prevFacts.filter(fact => fact.id !== factId));
    } catch (err) {
      console.error('Error deleting fact:', err);
      setError(err.message || 'Gagal menghapus fakta. Silakan coba lagi.');
    }
  };

  const startEdit = (fact) => {
    setEditingFact(fact);
    setEditContent(fact.content);
    setError('');
  };

  const cancelEdit = () => {
    setEditingFact(null);
    setEditContent('');
    setError('');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-200px)] p-6">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-10">Fact Management</h1>

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-md shadow-md" role="alert">
          <p className="font-bold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Form untuk Tambah Fakta Baru atau Edit Fakta */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-2xl p-6 mb-10"
      >
        <h2 className="text-2xl font-semibold text-gray-700 mb-6">
          {editingFact ? 'Edit Fakta' : 'Tambah Fakta Baru'}
        </h2>
        <form onSubmit={editingFact ? handleEditSubmit : handleAddSubmit} className="space-y-5">
          <div>
            <label htmlFor="factContent" className="block text-sm font-medium text-gray-600 mb-1">
              Konten Fakta
            </label>
            <textarea
              id="factContent"
              value={editingFact ? editContent : newFactContent}
              onChange={(e) => editingFact ? setEditContent(e.target.value) : setNewFactContent(e.target.value)}
              className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-150"
              rows="4"
              placeholder="Masukkan fakta menarik tentang anjing..."
              required
            />
          </div>
          <div className="flex items-center justify-end space-x-3">
            {editingFact && (
              <button
                type="button"
                onClick={cancelEdit}
                className="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-150"
              >
                Batal
              </button>
            )}
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150 disabled:opacity-60"
            >
              {isSubmitting ? 'Menyimpan...' : (editingFact ? 'Simpan Perubahan' : 'Tambah Fakta')}
            </button>
          </div>
        </form>
      </motion.div>

      {/* Daftar Fakta yang Ada */}
      <div className="bg-white rounded-xl shadow-2xl overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-semibold text-gray-700 mb-6">Daftar Fakta</h2>
          {facts.length === 0 && !loading && (
            <div className="text-center py-10 text-gray-500">
              <p className="text-lg">Belum ada fakta yang ditambahkan.</p>
              <p>Silakan tambahkan fakta baru menggunakan form di atas.</p>
            </div>
          )}
          {facts.length > 0 && (
            <div className="space-y-4">
              {facts.map((fact) => (
                <motion.div
                  key={fact.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3 }}
                  className="bg-gray-50 p-5 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 flex justify-between items-start"
                >
                  <p className="text-gray-800 leading-relaxed flex-1 mr-4">{fact.content}</p>
                  <div className="flex-shrink-0 flex gap-3">
                    <button
                      onClick={() => startEdit(fact)}
                      className="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors"
                      aria-label={`Edit fakta ${fact.id}`}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(fact.id)}
                      className="text-sm font-medium text-red-600 hover:text-red-800 transition-colors"
                      aria-label={`Hapus fakta ${fact.id}`}
                    >
                      Hapus
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FactManagement;