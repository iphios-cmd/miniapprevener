import { useEffect, useState, type CSSProperties } from 'react';

type Props = {
  visible: boolean;
};

/** Splash-загрузка в стиле Apple */
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
    const t = window.setTimeout(() => setMounted(false), 520);
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
        <p className="loading-title">Инструкция</p>
        <p className="loading-sub">Установка IPA на iOS</p>
        <div className="loading-spinner" role="progressbar" aria-label="Загрузка">
          {Array.from({ length: 8 }, (_, i) => (
            <span
              key={i}
              className="loading-spinner-blade"
              style={{ '--i': i } as CSSProperties}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
