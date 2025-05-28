import { motion } from 'framer-motion';
import { Link } from 'react-router-dom'; // Impor Link

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
              Dogs are our best friends
            </p>
            <Link to="/breeds"> {/* Tambahkan Link di sini */}
              <motion.button
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-8 py-3 rounded-full text-lg font-semibold hover:opacity-90 transition duration-300 shadow-lg"
              >
                  Jelajahi Ras Anjing
              </motion.button>
            </Link>
            <motion.p initial={{ y: 20, opacity: 0 }} animate={{y:0, opacity:1}} transition={{duration:0.8, delay:0.6}} className="text-sm text-gray-600 mt-4">
              Temukan informasi lengkap, fakta menarik, dan video lucu tentang sahabat setia kita.
            </motion.p>
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
        <div className="absolute top-10 -left-10 w-40 h-40 bg-cyan-300 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute bottom-10 -right-10 w-48 h-48 bg-blue-300 rounded-full opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/4 w-16 h-16 bg-yellow-300 rounded-full opacity-15 animate-ping delay-500"></div>

      </div>
    </div>
  );
};

export default HeroSection;