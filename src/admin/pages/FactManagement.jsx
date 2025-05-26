import { useState, useEffect } from 'react';

const FactManagement = () => {
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newFact, setNewFact] = useState('');

  useEffect(() => {
    fetchFacts();
  }, []);

  const fetchFacts = async () => {
    try {
      const response = await fetch('http://localhost:6543/api/admin/facts');
      const data = await response.json();
      setFacts(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching facts:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:6543/api/admin/facts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: newFact }),
      });
      if (response.ok) {
        fetchFacts();
        setNewFact('');
      }
    } catch (error) {
      console.error('Error adding fact:', error);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this fact?')) return;

    try {
      await fetch(`http://localhost:6543/api/admin/facts/${id}`, {
        method: 'DELETE',
      });
      fetchFacts();
    } catch (error) {
      console.error('Error deleting fact:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Fact Management</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Add New Fact</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Fact Content
            </label>
            <textarea
              value={newFact}
              onChange={(e) => setNewFact(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              rows="3"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Add Fact
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Existing Facts</h2>
          <div className="space-y-4">
            {facts.map((fact) => (
              <div
                key={fact.id}
                className="flex justify-between items-start p-4 bg-gray-50 rounded-lg"
              >
                <p className="flex-1">{fact.content}</p>
                <button
                  onClick={() => handleDelete(fact.id)}
                  className="ml-4 text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FactManagement;