import { useCallback, useEffect, useMemo } from 'react';

export function useTelegram() {
  const tg = useMemo(() => window.Telegram?.WebApp, []);

  useEffect(() => {
    if (!tg) return;
    tg.ready();
    tg.expand();

    const applyTheme = () => {
      const dark = tg.colorScheme === 'dark';
      document.documentElement.classList.toggle('dark-mode', dark);
      try {
        tg.setHeaderColor?.(dark ? '#0c0c0c' : '#f2f2f7');
        tg.setBackgroundColor?.(dark ? '#0c0c0c' : '#f2f2f7');
        if (typeof tg.setBottomBarColor === 'function') {
          tg.setBottomBarColor(dark ? '#0c0c0c' : '#f2f2f7');
        }
      } catch {
        /* older clients */
      }
    };

    applyTheme();
    tg.onEvent('themeChanged', applyTheme);
    return () => tg.offEvent('themeChanged', applyTheme);
  }, [tg]);

  const haptic = useCallback(
    (style: 'light' | 'medium' | 'heavy' = 'light') => {
      try {
        tg?.HapticFeedback?.impactOccurred(style);
      } catch {
        /* no haptics */
      }
    },
    [tg],
  );

  const hapticSuccess = useCallback(() => {
    try {
      tg?.HapticFeedback?.notificationOccurred('success');
    } catch {
      /* no haptics */
    }
  }, [tg]);

  const openBot = useCallback(
    (url: string) => {
      haptic('medium');
      if (tg?.openTelegramLink) {
        tg.openTelegramLink(url);
        return;
      }
      window.open(url, '_blank', 'noopener,noreferrer');
    },
    [tg, haptic],
  );

  return { tg, haptic, hapticSuccess, openBot };
}
