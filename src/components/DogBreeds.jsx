import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const DogBreeds = () => {
  const [breeds, setBreeds] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  
  const API_KEY = 'live_LjTiXLNveHjkoh664tkodk7f4L3A4pIPGVi8Bx0jUXvlpXI5bZiyzotUSHsOapxo';
  const LIMIT = 12; // Items per page

  const fetchBreeds = async (pageNumber) => {
    setLoading(true);
    try {
      const response = await fetch(
        `https://api.thedogapi.com/v1/breeds?limit=${LIMIT}&page=${pageNumber-1}${
          searchQuery ? `&q=${searchQuery}` : ''
        }`,
        {
          headers: {
            'x-api-key': API_KEY
          }
        }
      );
      const data = await response.json();
      
      if (pageNumber === 1) {
        setBreeds(data);
      } else {
        setBreeds(prev => [...prev, ...data]);
      }
      setHasMore(data.length === LIMIT);
    } catch (error) {
      console.error('Error fetching breeds:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setPage(1);
      fetchBreeds(1);
    }, 300); // Debounce search

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchBreeds(1);
  };

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">
      {/* Search Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Ras Anjing</h1>
          <p className="text-lg text-gray-600 mb-8">Temukan berbagai ras anjing dengan karakteristik uniknya</p>
          
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex shadow-lg rounded-full overflow-hidden">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Cari ras anjing..."
                className="flex-1 px-6 py-4 focus:outline-none"
              />
              <button
                type="submit"
                className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-8 py-4 hover:opacity-90 transition duration-300"
              >
                Cari
              </button>
            </div>
          </form>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {breeds.map((breed, index) => (
            <motion.div
              key={breed.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300"
            >
              <div className="relative h-64">
                <img 
                  src={breed.image?.url || '/placeholder-dog.jpg'} 
                  alt={breed.name}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">{breed.name}</h3>
                <Link 
                  to={`/breeds/${breed.id}`}
                  className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-2 px-4 rounded-lg font-medium hover:opacity-90 transition duration-300 inline-block text-center"
                >
                  Lihat Detail
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Load More Button */}
        {hasMore && (
          <div className="text-center mt-12">
            <button
              onClick={() => {
                const nextPage = page + 1;
                setPage(nextPage);
                fetchBreeds(nextPage);
              }}
              disabled={loading}
              className="bg-white text-blue-600 px-8 py-3 rounded-full shadow-lg font-medium hover:shadow-xl transition duration-300 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Muat Lebih Banyak'}
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center mt-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DogBreeds;