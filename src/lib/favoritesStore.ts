// src/lib/favoritesStore.ts
import { persistentMap } from '@nanostores/persistent';

// This creates a "store" - a reactive object that holds our favorite IDs.
// It's "persistent" because it automatically saves to localStorage.
// The key 'favorites' is where it's stored in the browser.
export const favoriteSummaries = persistentMap<Record<string, boolean>>('favorites', {});

// Function to add or remove a favorite.
// It takes the book's slug (e.g., 'atomic-habits') as an ID.
export function toggleFavorite(bookSlug: string) {
  // Check if the slug is already a key in our map
  if (favoriteSummaries.get()[bookSlug]) {
    // If it exists, remove it.
    // The `...favoriteSummaries.get()` part is a bit complex, but it's
    // how we update a part of the map without erasing the rest.
    const currentFavorites = { ...favoriteSummaries.get() };
    delete currentFavorites[bookSlug];
    favoriteSummaries.set(currentFavorites);
  } else {
    // If it doesn't exist, add it with a value of 'true'.
    favoriteSummaries.setKey(bookSlug, true);
  }
}

// We need to install a small library to make this work.
// We'll do that in the next step.