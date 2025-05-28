import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom'; // Import Link
import TikTokPreview from './TikTokPreview'; // Import TikTokPreview component
import InstagramPreview from './InstagramPreview';

// Helper function untuk mengambil item acak
const getRandomItems = (arr, n) => {
  if (!arr || arr.length === 0) return [];
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
};

const MainContent = () => {
  const [activeSlide, setActiveSlide] = useState(0);
  const [popularDogBreeds, setPopularDogBreeds] = useState([]);
  const [dogFacts, setDogFacts] = useState([]);
  const [dogViralVideos, setDogViralVideos] = useState([]);
  
  const [loadingBreeds, setLoadingBreeds] = useState(true);
  const [loadingFacts, setLoadingFacts] = useState(true);
  const [loadingVideos, setLoadingVideos] = useState(true);

  const API_BASE_URL = 'http://localhost:6544/api'; // Pastikan port backend benar

  useEffect(() => {
    // Fetch Popular Breeds
    const fetchPopularBreeds = async () => {
      try {
        setLoadingBreeds(true);
        const response = await fetch(`${API_BASE_URL}/popular-breeds`);
        const data = await response.json();
        if (response.ok) {
          setPopularDogBreeds(data.popular_breeds || []);
        } else {
          console.error("Failed to fetch popular breeds:", data.message);
          setPopularDogBreeds([]); // Atau set default jika gagal
        }
      } catch (error) {
        console.error('Error fetching popular breeds:', error);
        setPopularDogBreeds([]);
      } finally {
        setLoadingBreeds(false);
      }
    };

    // Fetch Facts
    const fetchFacts = async () => {
      try {
        setLoadingFacts(true);
        const response = await fetch(`${API_BASE_URL}/facts`); // Endpoint dari views/facts.py
        const result = await response.json();
        if (result.status === 'success' && result.data && result.data.facts) {
          setDogFacts(getRandomItems(result.data.facts, 5)); // Ambil 5 fakta acak
        } else {
          console.error("Failed to fetch facts:", result.message);
          setDogFacts([]);
        }
      } catch (error) {
        console.error('Error fetching facts:', error);
        setDogFacts([]);
      } finally {
        setLoadingFacts(false);
      }
    };

    // Fetch Viral Videos
    const fetchViralVideos = async () => {
      try {
        setLoadingVideos(true);
        const response = await fetch(`${API_BASE_URL}/videos`);
        const result = await response.json();
        if (result.status === 'success' && result.data && result.data.videos) {
          setDogViralVideos(result.data.videos.filter(video => video.isPublic));
        } else {
          console.error("Failed to fetch viral videos:", result.message);
          setDogViralVideos([]);
        }
      } catch (error) {
        console.error('Error fetching viral videos:', error);
        setDogViralVideos([]);
      } finally {
        setLoadingVideos(false);
      }
    };

    fetchPopularBreeds();
    fetchFacts();
    fetchViralVideos();
  }, []);

  // Update carousel otomatis untuk fakta
  useEffect(() => {
    if (dogFacts.length > 0) {
      const interval = setInterval(() => {
        setActiveSlide((prevSlide) => (prevSlide + 1) % dogFacts.length);
      }, 5000); // Ganti slide setiap 5 detik
      return () => clearInterval(interval);
    }
  }, [dogFacts]);


  return (
    <div className="py-16 bg-gradient-to-b from-white to-blue-50">
      {/* Dog Breeds Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-20">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Ras Anjing Populer</h2>
          <p className="text-lg text-gray-600">Temukan berbagai ras anjing pilihan dengan karakteristik uniknya</p>
        </div>
        
        {loadingBreeds ? (
          <p className="text-center">Memuat ras anjing populer...</p>
        ) : popularDogBreeds.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {popularDogBreeds.map((breed) => (
              <motion.div
                key={breed.id}
                whileHover={{ y: -10 }}
                transition={{ duration: 0.3 }}
                className="bg-white rounded-xl shadow-lg overflow-hidden transform hover:shadow-2xl transition-all duration-300 flex flex-col"
              >
                <div className="relative">
                  <img 
                    src={breed.image?.url || '/placeholder-dog.jpg'} // Gunakan breed.image.url, fallback ke placeholder
                    alt={breed.name} 
                    className="w-full h-56 object-cover"
                  />
                  <div className="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
                    Populer
                  </div>
                </div>
                
                <div className="p-6 flex-grow flex flex-col">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{breed.name}</h3>
                  <p className="text-gray-600 mb-4 text-sm flex-grow">{breed.description}</p>
                  {breed.traits && breed.traits.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {breed.traits.map((trait, index) => (
                        <span 
                          key={index}
                          className="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs"
                        >
                          {trait}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                
                <div className="px-6 pb-6 mt-auto"> {/* Tombol selalu di bawah */}
                  <Link to={`/breeds/${breed.id}`} className="w-full block">
                    <button className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-3 rounded-lg font-medium hover:opacity-90 transition duration-300">
                      Pelajari Lebih Lanjut
                    </button>
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <p className="text-center">Tidak ada ras anjing populer untuk ditampilkan.</p>
        )}
      </section>

      {/* Facts Carousel */}
      <section className="relative py-20 mb-20 bg-blue-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Fakta Menarik</h2>
            <p className="text-lg text-gray-600">Hal unik tentang anjing yang mungkin belum kamu ketahui</p>
          </div>
          
          {loadingFacts ? (
            <p className="text-center">Memuat fakta menarik...</p>
          ) : dogFacts.length > 0 ? (
            <div className="backdrop-blur-md bg-white/80 p-8 rounded-2xl shadow-xl min-h-[100px] flex flex-col justify-center">
              {dogFacts.map((fact, index) => (
                <motion.div
                  key={fact.id || index} // Gunakan fact.id jika tersedia
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ 
                    opacity: activeSlide === index ? 1 : 0,
                    y: activeSlide === index ? 0 : 20,
                    position: activeSlide === index ? 'relative' : 'absolute',
                  }}
                  transition={{ duration: 0.5 }}
                  className={`transition-all duration-500 w-full ${activeSlide === index ? 'block' : 'hidden'}`}
                >
                  <p className="text-2xl text-center text-gray-800 italic">{fact.content}</p>
                </motion.div>
              ))}
              
              <div className="flex justify-center mt-8 space-x-3">
                {dogFacts.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setActiveSlide(index)}
                    className={`w-3 h-3 rounded-full transition-all duration-300 ${
                      activeSlide === index 
                        ? 'bg-blue-600 scale-110' 
                        : 'bg-gray-300 hover:bg-gray-400'
                    }`}
                  />
                ))}
              </div>
            </div>
          ) : (
            <p className="text-center">Tidak ada fakta untuk ditampilkan.</p>
          )}
        </div>
      </section>

       {/* Video Viral Section */}
      <div className="bg-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Viral Dog Videos</h2>
            <p className="text-lg text-gray-600">Saksikan video-video anjing yang sedang viral</p>
          </div>
          
          {loadingVideos ? (
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4">Loading videos...</p>
            </div>
          ) : dogViralVideos.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">No viral videos available at the moment.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {dogViralVideos.map((video) => (
                <div key={video.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
                  <div className="relative">
                    {video.videoUrl.includes('instagram.com') ? (
                      <InstagramPreview postUrl={video.videoUrl} />
                    ) : (
                      <TikTokPreview videoUrl={video.videoUrl} />
                    )}
                  </div>
                  <div className="p-6">
                    <h3 className="font-semibold text-xl mb-2">{video.title}</h3>
                    {video.description && (
                      <p className="text-gray-600 text-sm mb-4">{video.description}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MainContent;