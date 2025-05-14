import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Facts = () => {
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const fetchFacts = async (pageNum = 1) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:6543/api/facts?page=${pageNum}&limit=5`);
      const result = await response.json();
      
      if (result.status === 'success') {
        if (pageNum === 1) {
          setFacts(result.data.facts);
        } else {
          setFacts(prev => [...prev, ...result.data.facts]);
        }
        setHasMore(result.data.pagination.hasMore);
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      setError('Gagal memuat fakta. Silakan coba lagi nanti.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFacts();
  }, []);

  const loadMore = () => {
    if (!loading && hasMore) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchFacts(nextPage);
    }
  };

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Fakta Menarik</h1>
          <p className="text-lg text-gray-600 mb-8">
            Temukan berbagai fakta unik dan menarik tentang anjing
          </p>
        </div>

        {error ? (
          <div className="text-center text-red-600 mb-8">{error}</div>
        ) : (
          <div className="grid gap-6">
            {facts.map((fact, index) => (
              <motion.div
                key={fact.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-blue-600 font-bold">{index + 1}</span>
                    </div>
                  </div>
                  <p className="text-gray-700 text-lg">{fact.content}</p>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {hasMore && (
          <div className="text-center mt-12">
            <button
              onClick={loadMore}
              disabled={loading}
              className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-8 py-3 rounded-full font-medium hover:opacity-90 transition duration-300 disabled:opacity-50"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                  <span>Loading...</span>
                </div>
              ) : (
                'Muat Lebih Banyak'
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Facts;