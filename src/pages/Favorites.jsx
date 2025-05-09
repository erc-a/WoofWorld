import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useFavorites } from '../contexts/FavoritesContext';

const Favorites = () => {
  const { favorites, removeFromFavorites } = useFavorites();

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Favorit Saya</h1>
          <p className="text-lg text-gray-600">
            Koleksi anjing favorit yang telah Anda simpan
          </p>
        </div>

        {favorites.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600 mb-6">
              Anda belum memiliki anjing favorit
            </p>
            <Link
              to="/breeds"
              className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-6 py-3 rounded-lg inline-block hover:opacity-90 transition duration-300"
            >
              Jelajahi Ras Anjing
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {favorites.map((dog) => (
              <motion.div
                key={dog.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                className="bg-white rounded-xl shadow-lg overflow-hidden"
              >
                <div className="relative">
                  <img
                    src={dog.image?.url}
                    alt={dog.name}
                    className="w-full h-56 object-cover"
                  />
                  <button
                    onClick={() => removeFromFavorites(dog.id)}
                    className="absolute top-4 right-4 p-2 bg-white rounded-full shadow-lg text-red-500 hover:text-red-600 transition-colors duration-300"
                  >
                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                    </svg>
                  </button>
                </div>

                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {dog.name}
                  </h3>
                  <p className="text-gray-600 mb-4">{dog.temperament}</p>
                  <Link
                    to={`/breeds/${dog.id}`}
                    className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-2 px-4 rounded-lg font-medium hover:opacity-90 transition duration-300 inline-block text-center"
                  >
                    Lihat Detail
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Favorites;