import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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
import Facts from './pages/Facts';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AdminLayout from './admin/layouts/AdminLayout';
import FactManagement from './admin/pages/FactManagement';
import VideoManagement from './admin/pages/VideoManagement';
import ForgotPassword from './pages/ForgotPassword';
import ChangePassword from './pages/ChangePassword';

function App() {
  return (
    <AuthProvider>
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
              <Route 
                path="/favorites" 
                element={
                  <ProtectedRoute>
                    <Favorites />
                  </ProtectedRoute>
                } 
              />
              <Route path="/facts" element={<Facts />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/change-password" element={<ChangePassword />} />
              <Route 
                path="/profile" 
                element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } 
              />              <Route 
                path="/admin" 
                element={
                  <ProtectedRoute requireAdmin={true}>
                    <AdminLayout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Navigate to="/admin/facts" replace />} />
                <Route path="facts" element={<FactManagement />} />
                <Route path="videos" element={<VideoManagement />} />
              </Route>
            </Routes>
            <Footer />
          </div>
        </Router>
      </FavoritesProvider>
    </AuthProvider>
  );
}

export default App;

