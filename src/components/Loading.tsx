import { useEffect, useState } from 'react';

type Props = {
  visible: boolean;
};

/** Splash-загрузка в стиле IPA Library miniapp */
export function Loading({ visible }: Props) {
  const [mounted, setMounted] = useState(visible);
  const [hiding, setHiding] = useState(false);

  useEffect(() => {
    if (visible) {
      setMounted(true);
      setHiding(false);
      return;
    }
    setHiding(true);
    const t = window.setTimeout(() => setMounted(false), 480);
    return () => window.clearTimeout(t);
  }, [visible]);

  if (!mounted) return null;

  return (
    <div
      id="loading"
      className={hiding ? 'hide' : ''}
      aria-busy={!hiding}
      aria-live="polite"
      aria-label="Загрузка"
    >
      <div className="loading-inner">
        <div className="loading-icon-wrap" aria-hidden="true">
          <span className="loading-icon" />
        </div>
        <div className="loading-title">Инструкция</div>
        <div className="loading-sub">Установка IPA на iOS</div>
        <div className="loading-bar" role="progressbar" aria-label="Загрузка">
          <span className="loading-bar-fill" />
        </div>
      </div>
    </div>
  );
}
