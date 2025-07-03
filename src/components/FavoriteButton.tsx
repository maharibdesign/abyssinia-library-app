// src/components/FavoriteButton.tsx

import { useStore } from '@nanostores/react';
import { favoriteSummaries, toggleFavorite } from '../lib/favoritesStore';

// This is the standard structure of a React component
export default function FavoriteButton({ bookSlug }: { bookSlug: string }) {
  // useStore is a React Hook. It subscribes the component to our store.
  // When the store changes, this component will automatically re-render.
  const $favorites = useStore(favoriteSummaries);
  const isFavorite = $favorites[bookSlug];

  // The handleClick function is called when the button is clicked.
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault(); // Prevents the link from navigating
    e.stopPropagation(); // Stops the event from "bubbling" to the parent card
    toggleFavorite(bookSlug); // Toggles the favorite status
  };

  // The component returns JSX (HTML-like syntax)
  return (
    <button 
      className={`favorite-btn ${isFavorite ? 'favorited' : ''}`} 
      onClick={handleClick}
      aria-label={`Favorite ${bookSlug}`}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>
    </button>
  );
}