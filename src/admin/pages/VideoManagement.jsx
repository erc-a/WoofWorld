import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import TikTokPreview from '../../components/TikTokPreview';

const VideoManagement = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  const fetchVideos = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:6544/api/videos', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch videos');
      const data = await response.json();
      setVideos(data.videos || []);
    } catch (error) {
      console.error('Error fetching videos:', error);
      setError('Failed to load videos');
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchVideos();
  }, [fetchVideos]);

  if (loading) return <div className="p-4">Loading...</div>;

  return (
    <div className="space-y-6 p-4">
      <h1 className="text-2xl font-bold">Video List</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => (
              <div key={video.id} className="bg-gray-50 rounded-lg p-4">
                <TikTokPreview 
                  videoUrl={video.videoUrl} 
                  title={video.title} 
                />
                <div className="mt-4">
                  <h3 className="font-semibold text-lg">{video.title}</h3>
                  <p className="text-gray-600 mt-1 text-sm">{video.description}</p>
                  <div className="flex justify-between items-center mt-3">
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      video.isPublic ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {video.isPublic ? 'Public' : 'Private'}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(video.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoManagement;