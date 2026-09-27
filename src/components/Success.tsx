import { useEffect } from 'react';
import { SUPPORT_URL } from '../config/steps';
import { Confetti } from './Confetti';

type Props = {
  onHome: () => void;
  onRestart: () => void;
  onSupport: (url: string) => void;
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
  hapticSuccess?: () => void;
};

export function Success({ onHome, onRestart, onSupport, haptic, hapticSuccess }: Props) {
  useEffect(() => {
    hapticSuccess?.();
  }, [hapticSuccess]);

  return (
    <main className="page success-page">
      <Confetti />

      <header className="section-header">
        <h1 className="section-title">Готово</h1>
        <p className="section-sub">Приложение установлено на iPhone</p>
      </header>

      <div className="hero-wrap">
        <div className="hero-card hero-card-success celebrate-pop">
          <div className="hero-art-stack" aria-hidden="true" />
          <div className="hero-simple-text">
            <div className="hero-title">Установка завершена</div>
            <div className="hero-sub">Ищите приложение на главном экране</div>
          </div>
          <div className="hero-art" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path
                d="M5 12.5 9.5 17 19 7.5"
                stroke="currentColor"
                strokeWidth="2.4"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>
      </div>

      <div className="home-actions success-actions">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => {
            haptic('medium');
            onHome();
          }}
        >
          На главную
        </button>
        <button type="button" className="btn btn-secondary" onClick={() => onSupport(SUPPORT_URL)}>
          Тех. Поддержка
        </button>
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => {
            haptic('light');
            onRestart();
          }}
        >
          Пройти ещё раз
        </button>
      </div>
    </main>
  );
}
