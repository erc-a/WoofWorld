import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-blue-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
        
        {/* Brand Section */}
        <div className="flex justify-center items-center mb-6">
          <img className="h-10 w-10" src="/fav_icon.svg" alt="WoofWorld Logo" />
          <span className="ml-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
            WoofWorld
          </span>
        </div>
        <p className="text-gray-600 max-w-md mx-auto mb-8">
          Temukan informasi lengkap, fakta menarik, dan semua yang perlu Anda ketahui tentang anjing kesayangan Anda.
        </p>

        {/* Quick Links */}
        <div className="flex justify-center flex-wrap gap-x-6 gap-y-2 mb-8">
          <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">Home</Link>
          <Link to="/breeds" className="text-gray-700 hover:text-blue-600 font-medium">Ras Anjing</Link>
          <Link to="/facts" className="text-gray-700 hover:text-blue-600 font-medium">Fakta</Link>
          <Link to="/favorites" className="text-gray-700 hover:text-blue-600 font-medium">Favorit</Link>
        </div>

        {/* Bottom Bar with Social Media */}
        <div className="border-t border-gray-200 mt-8 pt-8 flex flex-col sm:flex-row items-center justify-between">
          <p className="text-gray-500 text-sm mb-4 sm:mb-0">
            © {new Date().getFullYear()} WoofWorld. All rights reserved.
          </p>
          <div className="flex space-x-5">
            <a href="#" className="text-gray-400 hover:text-blue-600">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="#" className="text-gray-400 hover:text-blue-600">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a href="#" className="text-gray-400 hover:text-blue-600">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.237 2.636 7.855 6.356 9.312-.063-.125-.094-.25-.094-.375 0-.71.359-1.344 1.016-1.344.625 0 1.125.656 1.125 1.469 0 .812-.469 1.937-1.156 1.937-.938 0-1.625-.969-1.625-2.281 0-1.75 1.281-3.156 2.906-3.156 1.531 0 2.719 1.156 2.719 2.844 0 1.719-.906 3.656-2.156 3.656-1.188 0-2.031-.969-1.75-2.125.281-1.156.844-2.344.844-3.219 0-.812-.438-1.5-1.281-1.5-1.031 0-1.875.969-1.875 2.281 0 .594.125 1.031.313 1.469a7.89 7.89 0 00-.281-1.313c-.156-.594-.25-1.188-.25-1.813 0-2.031 1.5-3.875 4.344-3.875 2.875 0 4.969 2.031 4.969 4.813 0 2.969-1.813 5.344-4.344 5.344-1.375 0-2.625-.719-3.063-1.594l-.719 2.656c-.25.969-.75 2.313-1.156 3.094A10.01 10.01 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2z" clipRule="evenodd"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;