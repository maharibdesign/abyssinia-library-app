// src/lib/telegram.ts

// This function will be called to trigger haptic feedback
export function triggerImpact(style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') {
  // Check if we are inside Telegram
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.HapticFeedback.impactOccurred(style);
  }
}

// This function sets up all the Telegram-specific features
export function initTelegram() {
  // Check if the Telegram WebApp object is available
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;

    // Tell Telegram that the app is ready
    tg.ready();

    // ---- FEATURE 1: Theme Synchronization ----
    // Set the theme class on the <html> element based on Telegram's theme
    document.documentElement.className = tg.colorScheme;

    // Listen for theme changes and update the class
    tg.onEvent('themeChanged', () => {
      document.documentElement.className = tg.colorScheme;
    });

    // ---- FEATURE 2: Control the Back Button ----
    const backButton = tg.BackButton;
    // Show the button
    backButton.show();
    // When the button is clicked, go back in browser history
    backButton.onClick(() => {
      history.back();
    });

    // ---- FEATURE 3: Control the Main Button ----
    const mainButton = tg.MainButton;
    // Set the text and make it visible
    mainButton.setText('Show Favorites');
    mainButton.show();
    // When the button is clicked, navigate to our favorites page
    mainButton.onClick(() => {
      window.location.href = '/favorites';
    });
    
    // ---- FEATURE 4: Hide our web app's nav bar ----
    // The Telegram UI is better, so we hide our custom one.
    const navBar = document.querySelector('header'); // Find our <header> element
    if (navBar) {
      navBar.style.display = 'none';
      // Also remove the top padding from the body that was making space for it
      document.body.style.paddingTop = '1rem';
    }
  }
}