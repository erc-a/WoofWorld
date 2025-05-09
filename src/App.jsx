import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import MainContent from './components/MainContent';
import DogBreedDetail from './components/DogBreedDetail';
import './App.css';
import WaveDivider from './components/WaveDivider';
import Footer from './components/Footer';

function App() {
  return (
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
          <Route path="/breeds/:id" element={<DogBreedDetail />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;