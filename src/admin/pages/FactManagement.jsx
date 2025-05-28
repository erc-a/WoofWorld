import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';

const FactManagement = () => {
  const { user } = useAuth();
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newFact, setNewFact] = useState('');
  const [editingFact, setEditingFact] = useState(null);
  const [editContent, setEditContent] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFacts();
  }, []);  const fetchFacts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/admin/facts`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Failed to fetch facts');
      }
      const data = await response.json();
      setFacts(Array.isArray(data) ? data : data.facts || []);
      setError(''); // Clear any previous errors
      setLoading(false);
    } catch (error) {
      console.error('Error fetching facts:', error);
      setError(error.message || 'Failed to load facts. Please try again.');
      setLoading(false);
    }
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError('');      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/admin/facts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: newFact }),
      });      if (response.ok) {
        const result = await response.json();
        setFacts(prevFacts => [result, ...prevFacts]);
        setNewFact('');
        setError(''); // Clear any previous errors
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Failed to add fact');
      }
    } catch (error) {
      console.error('Error adding fact:', error);
      setError('Failed to add fact. Please try again.');
    }
  };

  const handleStartEdit = (fact) => {
    setEditingFact(fact.id);
    setEditContent(fact.content);
  };

  const handleCancelEdit = () => {
    setEditingFact(null);
    setEditContent('');
  };
  const handleSaveEdit = async (id) => {
    try {
      setError('');      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/admin/facts/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: editContent }),
      });
      if (response.ok) {
        const updatedFact = await response.json();
        setFacts(prevFacts => prevFacts.map(fact => 
          fact.id === id ? updatedFact : fact
        ));
        setEditingFact(null);
        setEditContent('');
        setError(''); // Clear any previous errors
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Failed to update fact');
      }
    } catch (error) {
      console.error('Error updating fact:', error);
      setError('Failed to update fact. Please try again.');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this fact?')) return;

    try {
      setError('');      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/admin/facts/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });      if (response.ok) {
        setFacts(prevFacts => prevFacts.filter(fact => fact.id !== id));
        setError(''); // Clear any previous errors
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Failed to delete fact');
      }
    } catch (error) {
      console.error('Error deleting fact:', error);
      setError('Failed to delete fact. Please try again.');
    }
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
      <h1 className="text-2xl font-bold mb-8">Fact Management</h1>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

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
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              rows="3"
              placeholder="Enter an interesting dog fact..."
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Add Fact
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-6">Existing Facts</h2>
          <div className="space-y-4">
            {facts.map((fact) => (
              <motion.div
                key={fact.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gray-50 rounded-lg overflow-hidden"
              >
                {editingFact === fact.id ? (
                  <div className="p-4">
                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      className="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      rows="3"
                    />
                    <div className="mt-3 flex gap-2 justify-end">
                      <button
                        onClick={() => handleSaveEdit(fact.id)}
                        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="p-4 flex justify-between items-start">
                    <p className="flex-1 text-gray-700">{fact.content}</p>
                    <div className="flex gap-2 ml-4">
                      <button
                        onClick={() => handleStartEdit(fact)}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(fact.id)}
                        className="text-red-600 hover:text-red-800 transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
            {facts.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No facts available. Add some interesting dog facts above!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FactManagement;