import { Icon } from './Icon';
import { VideoGuide } from './VideoGuide';
import { SUPPORT_URL, TOTAL_STEPS } from '../config/steps';

type Props = {
  onStart: () => void;
  onSupport: (url: string) => void;
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

export function Home({ onStart, onSupport, haptic }: Props) {
  return (
    <main className="page home-page">
      <header className="section-header">
        <h1 className="section-title">Инструкция</h1>
        <p className="section-sub">Установка IPA на iOS · {TOTAL_STEPS} шагов</p>
      </header>

      <div className="hero-wrap">
        <div className="hero-card">
          <div className="hero-art-stack" aria-hidden="true" />
          <div className="hero-simple-text">
            <div className="hero-title">
              Установите
              <br />
              приложение
            </div>
            <div className="hero-sub">Следуйте инструкции шаг за шагом. Весь процесс займёт 5 - 10 минут</div>
          </div>
          <div className="hero-art" aria-hidden="true">
            <span className="hero-art-icon" />
          </div>
        </div>
      </div>

      <div className="home-actions">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => {
            haptic('medium');
            onStart();
          }}
        >
          Начать установку
          <Icon name="arrow" />
        </button>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => onSupport(SUPPORT_URL)}
        >
          Тех. Поддержка
        </button>
      </div>

      <VideoGuide haptic={haptic} />
    </main>
  );
}
