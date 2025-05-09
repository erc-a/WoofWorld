import { createContext, useState, useContext, useEffect } from 'react';

const FavoritesContext = createContext();

export const FavoritesProvider = ({ children }) => {
  const [favorites, setFavorites] = useState(() => {
    const savedFavorites = localStorage.getItem('dogFavorites');
    return savedFavorites ? JSON.parse(savedFavorites) : [];
  });

  useEffect(() => {
    localStorage.setItem('dogFavorites', JSON.stringify(favorites));
  }, [favorites]);

  const addToFavorites = (dog) => {
    setFavorites(prev => {
      if (!prev.find(f => f.id === dog.id)) {
        return [...prev, dog];
      }
      return prev;
    });
  };

  const removeFromFavorites = (dogId) => {
    setFavorites(prev => prev.filter(dog => dog.id !== dogId));
  };

  const isFavorite = (dogId) => {
    return favorites.some(dog => dog.id === dogId);
  };

  return (
    <FavoritesContext.Provider value={{ favorites, addToFavorites, removeFromFavorites, isFavorite }}>
      {children}
    </FavoritesContext.Provider>
  );
};

export const useFavorites = () => useContext(FavoritesContext);