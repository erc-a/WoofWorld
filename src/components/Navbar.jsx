import { useState } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo - Positioned more to the left */}
          <div className="flex-shrink-0 -ml-4">
            <Link to="/" className="flex items-center">
              <img className="h-12 w-12" src="/public/fav_icon.svg" alt="WoofWorld Logo" />
              <span className="ml-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                WoofWorld
              </span>
            </Link>
          </div>

          {/* Center Menu Items */}
          <div className="hidden md:flex items-center justify-center flex-1">
            <div className="flex items-baseline space-x-8">
              <Link to="/" className="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium transition duration-300">
                Home
              </Link>
              <Link to="/breeds" className="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium transition duration-300">
                Ras Anjing
              </Link>
              <Link to="/facts" className="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium transition duration-300">
                Fakta
              </Link>
              <Link to="/favorites" className="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium transition duration-300">
                Favorit
              </Link>
            </div>
          </div>

          {/* Right Side - Login Button */}
          <div className="hidden md:flex items-center">
            <Link 
              to="/login" 
              className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-6 py-2.5 rounded-full text-sm font-medium hover:opacity-90 transition duration-300"
            >
              Login
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-blue-600 focus:outline-none"
            >
              <svg
                className="h-6 w-6"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 24 24"
              >
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link to="/" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-base font-medium">
              Home
            </Link>
            <Link to="/breeds" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-base font-medium">
              Ras Anjing
            </Link>
            <Link to="/facts" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-base font-medium">
              Fakta
            </Link>
            <Link to="/favorites" className="block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-base font-medium">
              Favorit
            </Link>
            <Link to="/login" className="block bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 rounded-full text-base font-medium">
              Login
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;