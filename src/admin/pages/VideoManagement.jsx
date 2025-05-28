import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import TikTokPreview from '../../components/TikTokPreview';
import { motion } from 'framer-motion'; // Untuk animasi konsisten

const VideoManagement = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth(); // Gunakan token dari AuthContext

  // State untuk modal dan form
  const [showModal, setShowModal] = useState(false);
  const [currentVideo, setCurrentVideo] = useState(null); // Untuk add/edit
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    videoUrl: '', // Frontend menggunakan videoUrl, backend video_url
    isPublic: true,
  });

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  const fetchVideos = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/videos`, { // Ganti ke endpoint admin
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.message || 'Gagal mengambil daftar video');
      }
      const data = await response.json();
      // Backend mengembalikan {videos: [...]}
      setVideos(data.videos || []);
    } catch (error) {
      console.error('Error fetching videos:', error);
      setError(error.message || 'Gagal memuat video');
      setVideos([]);
    } finally {
      setLoading(false);
    }
  }, [token, API_BASE_URL]);

  useEffect(() => {
    if (token) { // Hanya fetch jika token tersedia
      fetchVideos();
    } else {
      setLoading(false);
      setError("Autentikasi dibutuhkan untuk mengakses halaman ini.");
    }
  }, [fetchVideos, token]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const resetFormData = () => {
    setFormData({ title: '', description: '', videoUrl: '', isPublic: true });
  };

  const handleOpenAddModal = () => {
    setIsEditing(false);
    setCurrentVideo(null);
    resetFormData();
    setShowModal(true);
    setError('');
  };

  const handleOpenEditModal = (video) => {
    setIsEditing(true);
    setCurrentVideo(video);
    setFormData({
      title: video.title,
      description: video.description || '',
      videoUrl: video.videoUrl, // Frontend menggunakan videoUrl
      isPublic: video.isPublic,
    });
    setShowModal(true);
    setError('');
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentVideo(null);
    setIsEditing(false);
    resetFormData();
    setError('');
  };

  const handleSubmitVideo = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const url = isEditing 
      ? `${API_BASE_URL}/api/admin/videos/${currentVideo.id}`
      : `${API_BASE_URL}/api/admin/videos`;
    
    const method = isEditing ? 'PUT' : 'POST';

    // Backend mengharapkan video_url, bukan videoUrl
    const payload = {
      title: formData.title,
      description: formData.description,
      videoUrl: formData.videoUrl, // Kirim sebagai videoUrl, backend akan handle
      is_public: formData.isPublic, // Backend mungkin mengharapkan is_public
    };
    
    // Di backend views/admin/videos.py, saat add dan update, field yang diterima adalah:
    // title = data.get('title')
    // video_url = data.get('videoUrl') <-- sudah benar
    // description = data.get('description', '')
    // jadi 'videoUrl' dari frontend akan cocok.
    // Untuk isPublic, backend Model: `is_public = Column(Boolean, default=True, nullable=False)`
    // Backend View (update): Tidak ada update untuk `is_public` secara eksplisit, perlu ditambahkan jika mau diupdate.
    // Backend View (add): Tidak ada set `is_public` secara eksplisit, akan pakai default model.
    // Sebaiknya backend view juga menerima `is_public`.

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.message || `Gagal ${isEditing ? 'memperbarui' : 'menambahkan'} video`);
      }
      
      await response.json(); // Ambil data hasil (jika ada)
      fetchVideos(); // Refresh daftar video
      handleCloseModal();
    } catch (error) {
      console.error(`Error ${isEditing ? 'updating' : 'adding'} video:`, error);
      setError(error.message || `Terjadi kesalahan saat ${isEditing ? 'memperbarui' : 'menambahkan'} video`);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteVideo = async (videoId) => {
    if (!confirm('Apakah Anda yakin ingin menghapus video ini?')) return;
    setError('');
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/videos/${videoId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.message || 'Gagal menghapus video');
      }
      fetchVideos(); // Refresh daftar video
    } catch (error) {
      console.error('Error deleting video:', error);
      setError(error.message || 'Gagal menghapus video');
    } finally {
      setLoading(false);
    }
  };


  if (loading && videos.length === 0) return <div className="p-6 text-center">Memuat data video...</div>;

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Video Management</h1>
        <button
          onClick={handleOpenAddModal}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          Tambah Video
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-md">
          <p>{error}</p>
        </div>
      )}

      {/* Modal untuk Add/Edit Video */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
          >
            <h2 className="text-xl font-semibold mb-6">{isEditing ? 'Edit Video' : 'Tambah Video Baru'}</h2>
            <form onSubmit={handleSubmitVideo} className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">Judul</label>
                <input
                  type="text"
                  name="title"
                  id="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">Deskripsi</label>
                <textarea
                  name="description"
                  id="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="3"
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
              <div>
                <label htmlFor="videoUrl" className="block text-sm font-medium text-gray-700">URL Video (TikTok/Instagram)</label>
                <input
                  type="url"
                  name="videoUrl"
                  id="videoUrl"
                  value={formData.videoUrl}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="Contoh: https://www.tiktok.com/@user/video/123..."
                  required
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  name="isPublic"
                  id="isPublic"
                  checked={formData.isPublic}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label htmlFor="isPublic" className="ml-2 block text-sm text-gray-900">Publikasikan Video</label>
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                >
                  Batal
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Menyimpan...' : (isEditing ? 'Simpan Perubahan' : 'Tambah Video')}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}

      {/* Daftar Video */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6">
          {videos.length === 0 && !loading ? (
            <div className="text-center py-8 text-gray-500">
              Belum ada video yang ditambahkan.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {videos.map((video) => (
                <motion.div
                  key={video.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-gray-50 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="aspect-[9/16] w-full mb-3 overflow-hidden rounded">
                    <TikTokPreview 
                      videoUrl={video.videoUrl} 
                      title={video.title} 
                    />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg truncate" title={video.title}>{video.title}</h3>
                    <p className="text-gray-600 mt-1 text-sm truncate" title={video.description}>{video.description || 'Tidak ada deskripsi'}</p>
                    <div className="flex justify-between items-center mt-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        video.isPublic ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-800'
                      }`}>
                        {video.isPublic ? 'Publik' : 'Privat'}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(video.created_at).toLocaleDateString('id-ID', { year: 'numeric', month: 'short', day: 'numeric' })}
                      </span>
                    </div>
                    <div className="mt-4 flex gap-2 justify-end">
                      <button
                        onClick={() => handleOpenEditModal(video)}
                        className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteVideo(video.id)}
                        className="text-sm text-red-600 hover:text-red-800 transition-colors"
                      >
                        Hapus
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
         {loading && videos.length > 0 && (
            <div className="text-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto"></div>
            </div>
        )}
      </div>
    </div>
  );
};

export default VideoManagement;