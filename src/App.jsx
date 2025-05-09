import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import MainContent from './components/MainContent';
import DogBreeds from './components/DogBreeds';
import './App.css';
import WaveDivider from './components/WaveDivider';
import Footer from './components/Footer';
import DogBreedDetail from './components/DogBreedDetail';
import { FavoritesProvider } from './contexts/FavoritesContext';
import Favorites from './pages/Favorites';

function App() {
  return (
    <FavoritesProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            <Route path="/" element={
              <>
                <HeroSection />
                <WaveDivider />
                <MainContent />
              </>
            } />
            <Route path="/breeds" element={<DogBreeds />} />
            <Route path="/breeds/:id" element={<DogBreedDetail />} />
            <Route path="/favorites" element={<Favorites />} />
          </Routes>
          <Footer />
        </div>
      </Router>
    </FavoritesProvider>
  );
}

export default App;