import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const Facts = () => {
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFacts = async () => {
      try {
        const response = await fetch('http://localhost:6543/api/facts');
        const result = await response.json();
        
        if (result.status === 'success') {
          setFacts(result.data.facts);
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

    fetchFacts();
  }, []);

  return (
    <div className="pt-20 min-h-screen bg-gradient-to-b from-white to-blue-50">      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Fakta Menarik</h1>
          <p className="text-lg text-gray-600 mb-8">
            Temukan berbagai fakta unik dan menarik tentang anjing
          </p>
        </div>

        {error ? (
          <div className="text-center text-red-600 mb-8">{error}</div>
        ) : loading ? (
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {facts.map((fact, index) => (
              <motion.div
                key={fact.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
              >
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center mb-4">
                    <span className="text-blue-600 font-bold text-lg">{index + 1}</span>
                  </div>
                  <p className="text-gray-700 text-lg text-center">{fact.content}</p>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Facts;