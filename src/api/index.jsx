const API_BASE_URL = 'http://localhost:6544/api';

export const fetchFacts = async () => {
  const response = await fetch(`${API_BASE_URL}/facts/random?limit=5`);
  if (!response.ok) throw new Error('Failed to fetch facts');
  return response.json();
};

export const fetchPopularBreeds = async () => {
  const response = await fetch(`${API_BASE_URL}/breeds?limit=4`);
  if (!response.ok) throw new Error('Failed to fetch popular breeds');
  return response.json();
};

export const fetchViralVideos = async () => {
  const response = await fetch(`${API_BASE_URL}/videos/viral`);
  if (!response.ok) throw new Error('Failed to fetch viral videos');
  return response.json();
};
