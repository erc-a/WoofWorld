import { useState, useEffect } from 'react';

const BreedManagement = () => {
  const [breeds, setBreeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    breed_group: '',
    temperament: '',
    origin: '',
    life_span: '',
    weight_metric: '',
    height_metric: '',
  });

  useEffect(() => {
    fetchBreeds();
  }, []);

  const fetchBreeds = async () => {
    try {
      const response = await fetch('http://localhost:6543/api/admin/breeds');
      const data = await response.json();
      setBreeds(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching breeds:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:6543/api/admin/breeds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        fetchBreeds();
        setFormData({
          name: '',
          breed_group: '',
          temperament: '',
          origin: '',
          life_span: '',
          weight_metric: '',
          height_metric: '',
        });
      }
    } catch (error) {
      console.error('Error adding breed:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Breed Management</h1>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Add New Breed</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Form fields */}
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Add Breed
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Group
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {breeds.map((breed) => (
              <tr key={breed.id} className="border-t border-gray-200">
                <td className="px-6 py-4">{breed.name}</td>
                <td className="px-6 py-4">{breed.breed_group}</td>
                <td className="px-6 py-4">
                  <button className="text-red-600 hover:text-red-900">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BreedManagement;