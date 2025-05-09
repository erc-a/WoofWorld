import { useState } from 'react';
import { motion } from 'framer-motion';

const MainContent = () => {
  const [activeSlide, setActiveSlide] = useState(0);
  
  const facts = [
    "Anjing bisa memahami lebih dari 150 kata",
    "Hidung anjing selalu basah untuk membantu menyerap aroma kimia",
    "Anjing memiliki pendengaran yang 4 kali lebih sensitif dari manusia"
  ];

  return (
    <div className="py-16 bg-white">
      {/* Dog Breeds Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Ras Anjing Populer</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((item) => (
            <motion.div
              key={item}
              whileHover={{ scale: 1.05 }}
              className="bg-white rounded-lg shadow-lg overflow-hidden"
            >
              <img 
                src={`/dog-${item}.jpg`} 
                alt="Dog Breed" 
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h3 className="text-lg font-semibold">Golden Retriever</h3>
                <p className="text-gray-600">Anjing yang ramah dan pintar</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Facts Carousel */}
      <section className="bg-blue-50 py-16 mb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Fakta Menarik</h2>
          <div className="relative bg-white p-8 rounded-lg shadow-lg">
            {facts.map((fact, index) => (
              <div
                key={index}
                className={`transition-opacity duration-500 ${
                  activeSlide === index ? 'opacity-100' : 'opacity-0 hidden'
                }`}
              >
                <p className="text-xl text-center">{fact}</p>
              </div>
            ))}
            <div className="flex justify-center mt-6 space-x-2">
              {facts.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full ${
                    activeSlide === index ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                  onClick={() => setActiveSlide(index)}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Viral Videos Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Video Viral</h2>
        <div className="aspect-w-16 aspect-h-9">
          <iframe
            className="w-full h-[500px] rounded-lg"
            src="https://www.youtube.com/embed/your-video-id"
            title="Dog Video"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </section>
    </div>
  );
};

export default MainContent;