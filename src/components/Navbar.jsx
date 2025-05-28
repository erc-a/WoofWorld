// src/components/Navbar.jsx
import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Tambahkan useNavigate
import { AuthContext } from '../contexts/AuthContext';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate(); // Hook untuk navigasi

  const handleLogout = async () => {
    await logout();
    setIsProfileOpen(false); // Tutup dropdown setelah logout
    navigate('/'); // Arahkan ke halaman utama setelah logout
  };

  return (
    <nav className="bg-white shadow-lg fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex-shrink-0 -ml-4">
            <Link to="/" className="flex items-center">
              <img className="h-12 w-12" src="/public/fav_icon.svg" alt="WoofWorld Logo" />
              <span className="ml-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                WoofWorld
              </span>
            </Link>
          </div>

          {/* Menu Tengah */}
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
              {user && ( // Hanya tampilkan jika user login
                <Link to="/favorites" className="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium transition duration-300">
                  Favorit
                </Link>
              )}
            </div>
          </div>

          {/* Kanan: Tombol Login atau Profil */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="flex items-center space-x-3 focus:outline-none"
                >
                  <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg font-semibold border-2 border-white shadow-sm">
                    {user.name?.[0]?.toUpperCase() || '?'}
                  </div>
                  <span className="text-gray-700">{user.name}</span>
                </button>

                {isProfileOpen && (
                  <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="py-1">
                      <Link
                        to="/profile"
                        onClick={() => setIsProfileOpen(false)}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Edit Profil
                      </Link>
                      {user.role === 'admin' && ( // Tambahkan link ke Admin Dashboard jika admin
                        <Link
                          to="/admin"
                          onClick={() => setIsProfileOpen(false)}
                          className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Admin Dashboard
                        </Link>
                      )}
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/login"
                className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 rounded-lg hover:opacity-90 transition duration-300"
              >
                Masuk
              </Link>
            )}
          </div>

          {/* Tombol Menu Mobile */}
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

      {/* Menu Mobile */}
      {isOpen && (
        <div className="md:hidden bg-white shadow-md">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link to="/" onClick={() => setIsOpen(false)} className="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-md text-base font-medium">
              Home
            </Link>
            <Link to="/breeds" onClick={() => setIsOpen(false)} className="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-md text-base font-medium">
              Ras Anjing
            </Link>
            <Link to="/facts" onClick={() => setIsOpen(false)} className="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-md text-base font-medium">
              Fakta
            </Link>
            {user && (
              <Link to="/favorites" onClick={() => setIsOpen(false)} className="block text-gray-600 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-md text-base font-medium">
                Favorit
              </Link>
            )}
          </div>
          <div className="pt-2 pb-3 border-t border-gray-200">
            {user ? (
              <>
                <div className="flex items-center px-5 mb-2">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg font-semibold">
                      {user.name?.[0]?.toUpperCase() || '?'}
                    </div>
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium text-gray-800">{user.name}</div>
                    <div className="text-sm font-medium text-gray-500">{user.email}</div>
                  </div>
                </div>
                <div className="px-2 space-y-1">
                  <Link
                    to="/profile"
                    onClick={() => setIsOpen(false)}
                    className="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50"
                  >
                    Edit Profil
                  </Link>
                   {user.role === 'admin' && (
                    <Link
                      to="/admin"
                       onClick={() => setIsOpen(false)}
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50"
                    >
                      Admin Dashboard
                    </Link>
                  )}
                  <button
                    onClick={() => { handleLogout(); setIsOpen(false); }}
                    className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <div className="px-2">
                <Link
                  to="/login"
                  onClick={() => setIsOpen(false)}
                  className="block w-full text-center bg-gradient-to-r from-blue-600 to-cyan-500 text-white px-4 py-2 rounded-lg hover:opacity-90 transition duration-300"
                >
                  Masuk
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;