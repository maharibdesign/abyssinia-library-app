// src/lib/favoritesStore.ts
import { persistentMap } from '@nanostores/persistent';

// Use a prefix for the localStorage key to avoid conflicts and ensure it's unique.
const storageKey = 'abyssinia_favorites:';

// The persistentMap now correctly stores a Record where the value is the string '1'.
// This satisfies the library's type constraints.
export const favoriteSummaries = persistentMap<Record<string, '1'>>(storageKey, {});

/**
 * Adds or removes a favorite summary.
 * This version stores the string "1" as the value to be compatible with string-only storage.
 */
export function toggleFavorite(bookSlug: string) {
  // Get a mutable copy of the current favorites object.
  const currentFavorites = { ...favoriteSummaries.get() };

  if (currentFavorites[bookSlug]) {
    // If the key exists, it's a favorite. REMOVE the key entirely.
    delete currentFavorites[bookSlug];
  } else {
    // If the key doesn't exist, it's not a favorite. ADD it with the value "1".
    currentFavorites[bookSlug] = '1';
  }

  // Set the entire store to our new, modified object. This guarantees updates.
  favoriteSummaries.set(currentFavorites);
}