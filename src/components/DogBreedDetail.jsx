import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useFavorites } from '../contexts/FavoritesContext';
import { useAuth } from '../contexts/AuthContext';

const DogBreedDetail = () => {
  const { id } = useParams();
  const [breed, setBreed] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_KEY = 'live_LjTiXLNveHjkoh664tkodk7f4L3A4pIPGVi8Bx0jUXvlpXI5bZiyzotUSHsOapxo';
  const { isFavorite, addToFavorites, removeFromFavorites } = useFavorites();
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBreedDetail = async () => {
      try {
        const response = await fetch(
          'https://api.thedogapi.com/v1/breeds',
          {
            headers: {
              'x-api-key': API_KEY
            }
          }
        );
        const data = await response.json();
        const selectedBreed = data.find(b => b.id === parseInt(id));
        setBreed(selectedBreed);
      } catch (error) {
        console.error('Error fetching breed detail:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBreedDetail();
  }, [id]);

  const handleFavoriteClick = () => {
    if (!user) {
      navigate('/login', { state: { from: location.pathname } });
      return;
    }
    if (isFavorite(breed.id)) {
      removeFromFavorites(breed.id);
    } else {
      addToFavorites(breed);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!breed) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h2 className="text-2xl font-bold mb-4">Anjing tidak ditemukan</h2>
        <Link 
          to="/breeds"
          className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-6 py-2 rounded-full"
        >
          Kembali ke Daftar
        </Link>
      </div>
    );
  }

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl overflow-hidden"
        >
          <div className="md:flex">
            <div className="md:flex-shrink-0 md:w-1/2">
              <img
                className="h-96 w-full object-cover md:h-full"
                src={breed.image?.url}
                alt={breed.name}
              />
            </div>
            <div className="p-8 md:w-1/2">
              <div className="flex justify-between items-center">
                <div className="uppercase tracking-wide text-sm text-blue-600 font-semibold">
                  {breed.breed_group}
                </div>
                <button
                  onClick={handleFavoriteClick}
                  className={`p-2 rounded-full transition-colors duration-300 ${
                    isFavorite(breed.id)
                      ? 'text-red-500 hover:text-red-600'
                      : 'text-gray-400 hover:text-red-500'
                  }`}
                >
                  <svg
                    className="w-6 h-6 fill-current"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                </button>
              </div>
              <h1 className="mt-2 text-4xl font-bold text-gray-900">{breed.name}</h1>
              
              <div className="mt-4 space-y-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Temperamen</h2>
                  <p className="mt-1 text-gray-600">{breed.temperament}</p>
                </div>
                
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Asal</h2>
                  <p className="mt-1 text-gray-600">{breed.origin || 'Tidak diketahui'}</p>
                </div>
                
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Umur</h2>
                  <p className="mt-1 text-gray-600">{breed.life_span}</p>
                </div>
                
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Berat</h2>
                  <p className="mt-1 text-gray-600">
                    {breed.weight?.metric} kg ({breed.weight?.imperial} lbs)
                  </p>
                </div>
                
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Tinggi</h2>
                  <p className="mt-1 text-gray-600">
                    {breed.height?.metric} cm ({breed.height?.imperial} inches)
                  </p>
                </div>
              </div>

              <div className="mt-8">
                <Link
                  to="/breeds"
                  className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-6 py-3 rounded-lg inline-block hover:opacity-90 transition duration-300"
                >
                  Kembali ke Daftar
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default DogBreedDetail;