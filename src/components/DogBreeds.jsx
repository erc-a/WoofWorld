import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const DogBreeds = () => {
  const [breeds, setBreeds] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false); // Di set false awalnya, akan true saat fetching
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  
  // API_KEY sebaiknya tidak disimpan di frontend. Backend yang akan menggunakannya.
  // const API_KEY = 'live_LjTiXLNveHjkoh664tkodk7f4L3A4pIPGVi8Bx0jUXvlpXI5bZiyzotUSHsOapxo';
  const LIMIT = 12; // Items per page

  const fetchBreeds = async (pageNumber, currentSearchQuery) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        limit: LIMIT.toString(),
        page: (pageNumber - 1).toString(), // API mungkin 0-indexed untuk halaman
      });
      if (currentSearchQuery) {
        params.append('q', currentSearchQuery);
      }
      
      // Panggil backend Anda, bukan TheDogAPI secara langsung
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/breeds?${params.toString()}`
      );
      const data = await response.json(); // Backend Anda diharapkan mengembalikan { breeds: [...] }
      
      const newBreeds = data.breeds || data; // TheDogAPI /breeds/search mengembalikan array langsung

      if (pageNumber === 1) {
        setBreeds(newBreeds);
      } else {
        // Hindari duplikasi jika item yang sama ter-fetch lagi (jarang terjadi dengan paging yang benar)
        setBreeds(prev => {
          const existingIds = new Set(prev.map(b => b.id));
          const filteredNewBreeds = newBreeds.filter(b => !existingIds.has(b.id));
          return [...prev, ...filteredNewBreeds];
        });
      }
      setHasMore(newBreeds.length === LIMIT);
    } catch (error) {
      console.error('Error fetching breeds:', error);
      setBreeds([]); // Reset breeds jika ada error
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch breeds ketika searchQuery berubah (dengan debounce)
    const timer = setTimeout(() => {
      setPage(1); // Reset halaman ke 1 setiap kali ada pencarian baru
      fetchBreeds(1, searchQuery);
    }, 300); // Debounce 300ms

    return () => clearTimeout(timer);
  }, [searchQuery]); // Hanya jalankan jika searchQuery berubah

  useEffect(() => {
    // Fetch breeds untuk halaman selanjutnya (infinite scroll/load more)
    // Jangan fetch di sini jika page === 1 karena sudah dihandle oleh useEffect di atas
    if (page > 1) {
      fetchBreeds(page, searchQuery);
    }
  }, [page]); // Hanya jalankan jika page berubah (dan bukan perubahan searchQuery)


  const handleSearchSubmit = (e) => {
    e.preventDefault();
    // searchQuery sudah di-update oleh onChange, useEffect di atas akan handle fetch
    // Jika ingin fetch langsung di sini:
    setPage(1);
    fetchBreeds(1, searchQuery);
  };

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">
      {/* Search Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Ras Anjing</h1>
          <p className="text-lg text-gray-600 mb-8">Temukan berbagai ras anjing dengan karakteristik uniknya</p>
          
          <form onSubmit={handleSearchSubmit} className="max-w-2xl mx-auto">
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
        {loading && breeds.length === 0 && ( // Tampilkan loading awal hanya jika belum ada breed
          <div className="flex justify-center mt-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        )}

        {breeds.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {breeds.map((breed, index) => (
              <motion.div
                key={`${breed.id}-${index}`} // Pastikan key unik jika ada kemungkinan ID duplikat sementara
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
        )}

        {!loading && breeds.length === 0 && searchQuery && (
          <div className="text-center mt-12">
            <p className="text-lg text-gray-600">Tidak ada ras anjing yang cocok dengan "{searchQuery}".</p>
          </div>
        )}
        
        {!loading && breeds.length === 0 && !searchQuery && (
             <div className="text-center mt-12">
                <p className="text-lg text-gray-600">Tidak ada ras anjing tersedia saat ini.</p>
            </div>
        )}


        {/* Load More Button */}
        {hasMore && !loading && breeds.length > 0 && (
          <div className="text-center mt-12">
            <button
              onClick={() => {
                setPage(prevPage => prevPage + 1);
              }}
              disabled={loading}
              className="bg-white text-blue-600 px-8 py-3 rounded-full shadow-lg font-medium hover:shadow-xl transition duration-300 disabled:opacity-50"
            >
              {loading ? 'Memuat...' : 'Muat Lebih Banyak'}
            </button>
          </div>
        )}
        
        {loading && breeds.length > 0 && ( // Tampilkan loading di bawah jika sudah ada breed
          <div className="flex justify-center mt-8">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        )}

      </div>
    </div>
  );
};

export default DogBreeds;