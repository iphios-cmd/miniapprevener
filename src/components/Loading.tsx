import type { CSSProperties } from 'react';

/** Красивый iOS-спиннер с мягким свечением */
export function Loading({ visible }: { visible: boolean }) {
  if (!visible) return null;

  return (
    <div id="loading" aria-busy="true" aria-live="polite">
      <div className="loading-stage">
        <div className="loading-glow" aria-hidden="true" />
        <div className="apple-spinner" role="progressbar" aria-label="Загрузка">
          {Array.from({ length: 12 }, (_, i) => (
            <i key={i} style={{ '--i': i } as CSSProperties} />
          ))}
        </div>
      </div>
    </div>
  );
}
