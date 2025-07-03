// src/lib/favoritesStore.ts
import { persistentMap } from '@nanostores/persistent';

// The store definition remains the same.
export const favoriteSummaries = persistentMap<Record<string, boolean>>('favorites', {});

/**
 * Adds or removes a favorite summary.
 * This new version uses a more robust method to ensure UI components always update.
 */
export function toggleFavorite(bookSlug: string) {
  // First, get a mutable copy of the current favorites object.
  const currentFavorites = { ...favoriteSummaries.get() };

  if (currentFavorites[bookSlug]) {
    // --- The book IS currently a favorite, so we REMOVE it. ---
    delete currentFavorites[bookSlug];
  } else {
    // --- The book IS NOT a favorite, so we ADD it. ---
    currentFavorites[bookSlug] = true;
  }

  // Finally, set the entire store to our new, modified object.
  // This guarantees that any listening components will be notified of the change.
  favoriteSummaries.set(currentFavorites);
}