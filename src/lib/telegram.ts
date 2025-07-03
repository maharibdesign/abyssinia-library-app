// src/lib/telegram.ts
export function triggerImpact(style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.HapticFeedback.impactOccurred(style);
  }
}

export function initTelegram() {
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    tg.ready();
    document.documentElement.className = tg.colorScheme;
    tg.onEvent('themeChanged', () => {
      document.documentElement.className = tg.colorScheme;
    });
    
    // Setup the back button
    const backButton = tg.BackButton;
    backButton.show();
    backButton.onClick(() => history.back());
    
    // HIDE the main button since we have no favorites page
    const mainButton = tg.MainButton;
    mainButton.hide();

    // Hide our custom nav bar
    const navBar = document.querySelector('header');
    if (navBar) {
      navBar.style.display = 'none';
      document.body.style.paddingTop = '1rem';
    }
  }
}