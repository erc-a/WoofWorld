import { motion } from 'framer-motion';

const HeroSection = () => {
  return (
    <div className="relative h-[600px] overflow-hidden bg-blue-100">
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        {/* Content Container with Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 h-full items-center">   
          {/* Left Side - Text Content */}
          <motion.div 
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-left z-10"
          >
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold mb-4">
              <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                WoofWorld
              </span>
            </h1>
            <p className="text-2xl sm:text-3xl md:text-4xl text-gray-700 font-light mb-8">
              Dog is Our Bestfriend
            </p>
            <motion.button
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-8 py-3 rounded-full text-lg font-semibold hover:opacity-90 transition duration-300 shadow-lg"
            >
                Get Started
            </motion.button>
          </motion.div>

          {/* Right Side - Dog Image */}
          <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="hidden md:block relative h-full"
          >
            <img 
              src="/public/Background.png" 
              alt="Happy Dog" 
              className="absolute bottom-0 right-0 h-[90%] object-contain"
            />
          </motion.div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-20 right-10 w-20 h-20 bg-blue-500 rounded-full opacity-10"></div>
        <div className="absolute bottom-20 left-10 w-32 h-32 bg-cyan-500 rounded-full opacity-10"></div>
      </div>
    </div>
  );
};

export default HeroSection;