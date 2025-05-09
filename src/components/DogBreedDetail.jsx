import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

const DogBreedDetail = () => {
  const { id } = useParams();
  const [isFavorite, setIsFavorite] = useState(false);
  const [comment, setComment] = useState('');
  const [comments, setComments] = useState([]);

  // Mock data - replace with actual API call
  const breedData = {
    name: 'Golden Retriever',
    origin: 'Scotland',
    temperament: 'Friendly, Intelligent, Devoted',
    description: 'The Golden Retriever is a large-sized breed of dog bred as gun dogs to retrieve shot waterfowl and upland game birds during hunting and shooting parties, and were named retriever because of their ability to retrieve shot game undamaged.',
    imageUrl: '/golden-retriever.jpg',
    videoUrl: 'https://www.youtube.com/embed/your-video-id'
  };

  const handleAddComment = (e) => {
    e.preventDefault();
    if (comment.trim()) {
      setComments([
        ...comments,
        { id: Date.now(), text: comment, user: 'User', timestamp: new Date() }
      ]);
      setComment('');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Breed Header */}
        <div className="relative">
          <img 
            src={breedData.imageUrl} 
            alt={breedData.name}
            className="w-full h-[500px] object-cover rounded-xl"
          />
          <button
            onClick={() => setIsFavorite(!isFavorite)}
            className="absolute top-4 right-4 bg-white p-3 rounded-full shadow-lg"
          >
            <svg 
              className={`w-6 h-6 ${isFavorite ? 'text-red-500' : 'text-gray-400'}`}
              fill={isFavorite ? 'currentColor' : 'none'}
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
        </div>

        {/* Breed Information */}
        <div className="mt-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{breedData.name}</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold mb-2">Asal</h2>
              <p className="text-gray-600 mb-4">{breedData.origin}</p>
              <h2 className="text-xl font-semibold mb-2">Temperamen</h2>
              <p className="text-gray-600 mb-4">{breedData.temperament}</p>
              <h2 className="text-xl font-semibold mb-2">Deskripsi</h2>
              <p className="text-gray-600">{breedData.description}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-4">Video</h2>
              <div className="aspect-w-16 aspect-h-9">
                <iframe
                  src={breedData.videoUrl}
                  className="w-full h-[300px] rounded-lg"
                  allowFullScreen
                ></iframe>
              </div>
            </div>
          </div>
        </div>

        {/* Comments Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold mb-6">Komentar</h2>
          <form onSubmit={handleAddComment} className="mb-8">
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              className="w-full p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Tambahkan komentar..."
              rows="4"
            ></textarea>
            <button
              type="submit"
              className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-300"
            >
              Kirim Komentar
            </button>
          </form>

          {/* Comments List */}
          <div className="space-y-6">
            {comments.map((comment) => (
              <div key={comment.id} className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold">{comment.user}</h3>
                    <p className="text-gray-600 mt-1">{comment.text}</p>
                  </div>
                  <button className="text-gray-400 hover:text-red-500">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
                <p className="text-sm text-gray-400 mt-2">
                  {new Date(comment.timestamp).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default DogBreedDetail;