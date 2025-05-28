import { useState, useEffect } from 'react';

const BreedManagement = () => {
  const [breeds, setBreeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const API_KEY = 'live_LjTiXLNveHjkoh664tkodk7f4L3A4pIPGVi8Bx0jUXvlpXI5bZiyzotUSHsOapxo';

  const fetchBreeds = async () => {
    try {
      const endpoint = searchQuery
        ? `https://api.thedogapi.com/v1/breeds/search?q=${searchQuery}`
        : 'https://api.thedogapi.com/v1/breeds';
        
      const response = await fetch(endpoint, {
        headers: {
          'x-api-key': API_KEY
        }
      });
      const data = await response.json();
      setBreeds(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching breeds:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchBreeds();
    }, 300); // Debounce search

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchQuery]);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Breed Management</h1>
        <div className="text-sm text-gray-600">
          * Data from TheDogAPI
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex gap-4">
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearch}
            placeholder="Search breeds..."
            className="flex-1 px-4 py-2 border rounded-lg"
          />
        </div>

        <div className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {breeds.map((breed) => (
              <div key={breed.id} className="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-900">{breed.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{breed.breed_group || 'No group specified'}</p>
                  <div className="mt-2 space-y-1">
                    <p className="text-sm">
                      <span className="font-medium">Temperament:</span> {breed.temperament || 'Not specified'}
                    </p>
                    <p className="text-sm">
                      <span className="font-medium">Life Span:</span> {breed.life_span || 'Not specified'}
                    </p>
                    <p className="text-sm">
                      <span className="font-medium">Origin:</span> {breed.origin || 'Not specified'}
                    </p>
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

export default BreedManagement;