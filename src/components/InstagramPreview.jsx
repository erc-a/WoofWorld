import React from 'react';

const InstagramPreview = ({ postUrl }) => {
  const getEmbedUrl = (url) => {
    try {
      const cleanUrl = url.replace(/\/$/, '').split('?')[0];
      const matches = cleanUrl.match(/instagram\.com\/(p|reel)\/([^/]+)/);
      if (matches) {
        const [_, type, id] = matches;
        return `https://www.instagram.com/${type}/${id}/embed`;
      }
      return url;
    } catch (error) {
      console.error('Error processing Instagram URL:', error);
      return url;
    }
  };

  return (
    <div className="aspect-[9/16] w-full">
      <iframe
        title="Instagram Post"
        src={getEmbedUrl(postUrl)}
        className="w-full h-full"
        allowFullScreen
        scrolling="no"
        frameBorder="0"
        allow="autoplay; clipboard-write; encrypted-media; picture-in-picture"
      />
    </div>
  );
};

export default InstagramPreview;