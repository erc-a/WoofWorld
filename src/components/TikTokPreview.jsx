import React from 'react';

const TikTokPreview = ({ videoUrl }) => {
  // Transform URL to correct embed format
  const getEmbedUrl = (url) => {
    try {
      // If it's already an embed URL, return as is
      if (url.includes('/embed/')) return url;
      
      // Handle normal TikTok URL with video ID
      if (url.includes('/video/')) {
        const videoId = url.split('/video/')[1]?.split('?')[0];
        return `https://www.tiktok.com/embed/v2/${videoId}`;
      }

      // Handle profile URL
      const username = url.match(/@([^?]+)/)?.[1];
      if (username) {
        return `https://www.tiktok.com/embed/@${username}`;
      }

      return url;
    } catch (error) {
      console.error('Error processing TikTok URL:', error);
      return url;
    }
  };

  const embedUrl = getEmbedUrl(videoUrl);
  console.log('Embed URL:', embedUrl); // For debugging

  return (
    <div className="aspect-[9/16] w-full">
      <iframe
        src={embedUrl}
        className="w-full h-full"
        allowFullScreen
        frameBorder="0"
        sandbox="allow-scripts allow-same-origin allow-popups"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      />
    </div>
  );
};

export default TikTokPreview;
