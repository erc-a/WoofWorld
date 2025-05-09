import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const MainContent = () => {
  const [activeSlide, setActiveSlide] = useState(0);

  useEffect(() => {
  const tiktokScript = document.createElement('script');
  tiktokScript.src = "https://www.tiktok.com/embed.js";
  tiktokScript.async = true;
  document.body.appendChild(tiktokScript);

  const igScript = document.createElement('script');
  igScript.src = "https://www.instagram.com/embed.js";
  igScript.async = true;
  document.body.appendChild(igScript);
  }, []);

  const dogBreeds = [
    {
      id: 1,
      name: "Golden Retriever",
      description: "Anjing yang ramah dan pintar",
      image: "/dog-1.jpg",
      traits: ["Friendly", "Intelligent", "Loyal"]
    },
    {
      id: 2,
      name: "German Shepherd",
      description: "Anjing yang setia dan penjaga",
      image: "/dog-2.jpg",
      traits: ["Protective", "Smart", "Brave"]
    },
    {
      id: 3,
      name: "Siberian Husky",
      description: "Anjing yang energetik dan cantik",
      image: "/dog-3.jpg",
      traits: ["Energetic", "Independent", "Friendly"]
    },
    {
      id: 4,
      name: "Pomeranian",
      description: "Anjing mungil yang menggemaskan",
      image: "/dog-4.jpg",
      traits: ["Playful", "Alert", "Sociable"]
    }
  ];

  const facts = [
    "Anjing bisa memahami lebih dari 150 kata",
    "Hidung anjing selalu basah untuk membantu menyerap aroma kimia",
    "Anjing memiliki pendengaran yang 4 kali lebih sensitif dari manusia"
  ];

  const viralVideos = [
    {
      id: 1,
      title: "Golden Main Bola",
      breed: "Golden Retriever",
      videoUrl: "https://www.tiktok.com/@certifiedfreedomlover/video/7483970811037240582",
      thumbnail: "/video-thumb-1.jpg",
      author: "@goldenlovers",
      likes: "1.2M"
    },
    {
      id: 2,
      title: "Husky Bernyanyi",
      breed: "Siberian Husky",
      videoUrl: "https://www.instagram.com/reel/C5tc72viPWV",
      thumbnail: "/video-thumb-2.jpg",
      author: "@huskycute",
      likes: "890K"
    },
    {
      id: 3,
      title: "Pom Lucu Berputar",
      breed: "Pomeranian",
      videoUrl: "https://www.tiktok.com/embed/v2/7123456791",
      thumbnail: "/video-thumb-3.jpg",
      author: "@pompomworld",
      likes: "750K"
    }
  ];

  return (
    <div className="py-16 bg-gradient-to-b from-white to-blue-50">
      {/* Dog Breeds Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-20">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Ras Anjing Populer</h2>
          <p className="text-lg text-gray-600">Temukan berbagai ras anjing pilihan dengan karakteristik uniknya</p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {dogBreeds.map((breed) => (
            <motion.div
              key={breed.id}
              whileHover={{ y: -10 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden transform hover:shadow-2xl transition-all duration-300"
            >
              <div className="relative">
                <img 
                  src={breed.image} 
                  alt={breed.name} 
                  className="w-full h-56 object-cover"
                />
                <div className="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
                  Popular
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{breed.name}</h3>
                <p className="text-gray-600 mb-4">{breed.description}</p>
                <div className="flex flex-wrap gap-2">
                  {breed.traits.map((trait, index) => (
                    <span 
                      key={index}
                      className="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm"
                    >
                      {trait}
                    </span>
                  ))}
                </div>
              </div>
              
              <div className="px-6 pb-6">
                <button className="w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-3 rounded-lg font-medium hover:opacity-90 transition duration-300">
                  Pelajari Lebih Lanjut
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Facts Carousel */}
      <section className="relative py-20 mb-20 bg-blue-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Fakta Menarik</h2>
            <p className="text-lg text-gray-600">Hal unik tentang anjing yang mungkin belum kamu ketahui</p>
          </div>
          
          <div className="backdrop-blur-md bg-white/80 p-8 rounded-2xl shadow-xl">
            {facts.map((fact, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ 
                  opacity: activeSlide === index ? 1 : 0,
                  y: activeSlide === index ? 0 : 20
                }}
                transition={{ duration: 0.5 }}
                className={`transition-all duration-500 ${activeSlide === index ? 'block' : 'hidden'}`}
              >
                <p className="text-2xl text-center text-gray-800 italic">{fact}</p>
              </motion.div>
            ))}
            
            <div className="flex justify-center mt-8 space-x-3">
              {facts.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setActiveSlide(index)}
                  className={`w-4 h-4 rounded-full transition-all duration-300 ${
                    activeSlide === index 
                      ? 'bg-blue-600 scale-110' 
                      : 'bg-gray-300 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Video Viral Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-20">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Video Viral</h2>
          <p className="text-lg text-gray-600">Tonton video menarik seputar anjing</p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {viralVideos.map((video) => (
            <motion.div
              key={video.id}
              whileHover={{ y: -5 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden"
            >
              <div className="relative aspect-[9/16] bg-gray-100">
                <blockquote
                  className="tiktok-embed"
                  cite={video.videoUrl}
                  data-video-id={video.videoUrl.split("/").pop()}
                  style={{ width: "100%", height: "100%" }}
                >
                  <section>
                    <a href={video.videoUrl} target="_blank" rel="noopener noreferrer">
                      Watch Video
                    </a>
                  </section>
                </blockquote>
              </div>
              
              <div className="p-5">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{video.title}</h3>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-blue-600 font-medium">{video.breed}</span>
                </div>
                <div className="flex items-center text-gray-500 text-sm">
                  <span>{video.author}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default MainContent;
