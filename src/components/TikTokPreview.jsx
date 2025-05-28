import React from 'react';

const TikTokPreview = ({ videoUrl, title }) => {
  const handleClick = () => {
    window.open(videoUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <div 
      onClick={handleClick}
      className="cursor-pointer relative overflow-hidden rounded-lg bg-gray-100 hover:bg-gray-200 transition-all"
    >
      <div className="aspect-[9/16] flex items-center justify-center p-4">
        <div className="text-center">
          <svg 
            className="w-12 h-12 mx-auto text-gray-400 mb-2" 
            fill="currentColor" 
            viewBox="0 0 24 24"
          >
            <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.43v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 015.2-2.32V9.39a8.33 8.33 0 005.65 3.24V2h-.42z"/>
          </svg>
          <p className="text-sm font-medium text-gray-900 truncate max-w-[200px]">{title}</p>
          <p className="text-xs text-gray-500 mt-1">Click to watch on TikTok</p>
        </div>
      </div>
    </div>
  );
};

export default TikTokPreview;
