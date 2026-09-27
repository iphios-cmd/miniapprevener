import { useEffect, useRef } from 'react';
import { STEPS, TOTAL_STEPS } from '../config/steps';
import { highlightInstruction } from '../lib/highlightInstruction';
import { Icon } from './Icon';

type Props = {
  step: number;
  onBack: () => void;
  onNext: () => void;
  onAction: (url: string) => void;
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

const phaseFor = (step: number) =>
  step <= 5 ? 'Подготовка' : step <= 10 ? 'Импорт' : 'Установка';

export function Wizard({ step, onBack, onNext, onAction, haptic }: Props) {
  const contentRef = useRef<HTMLDivElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const imageDialogRef = useRef<HTMLDialogElement>(null);
  const current = STEPS[step - 1];
  const isFirst = step === 1;
  const isLast = step === TOTAL_STEPS;

  useEffect(() => {
    contentRef.current?.scrollTo({ top: 0 });
    headingRef.current?.focus({ preventScroll: true });
    const next = STEPS[step];
    if (next) {
      const preload = new Image();
      preload.src = next.image;
    }
  }, [step]);

  if (!current) return null;

  return (
    <div className="wizard">
      <header className="wizard-header">
        <div className="wizard-heading">
          <div className="section-title wizard-title">Инструкция</div>
          <div className="section-sub">
            Шаг {step} из {TOTAL_STEPS} · {phaseFor(step)}
          </div>
        </div>
        <span className="wizard-progress-meta">{String(step).padStart(2, '0')}</span>
      </header>

      <div
        className="progress-track"
        role="progressbar"
        aria-label="Прогресс инструкции"
        aria-valuemin={0}
        aria-valuemax={TOTAL_STEPS}
        aria-valuenow={step}
        aria-valuetext={`Шаг ${step} из ${TOTAL_STEPS}`}
      >
        {STEPS.map((item) => (
          <span
            key={item.id}
            className={`progress-segment${item.id <= step ? ' is-complete' : ''}${item.id === step ? ' is-current' : ''}`}
          />
        ))}
      </div>

      <main className="wizard-scroll" ref={contentRef}>
        <article key={current.id} className="wizard-step">
          <h1 ref={headingRef} tabIndex={-1} className="step-title">
            {current.title}
          </h1>

          <figure className="step-visual card">
            <button
              type="button"
              className="step-image-button"
              aria-label={`Увеличить иллюстрацию: ${current.title}`}
              onClick={() => {
                haptic('light');
                imageDialogRef.current?.showModal();
              }}
            >
              <img
                className="step-image"
                src={current.image}
                alt={`Шаг ${step}: ${current.title}`}
                width="1672"
                height="941"
                decoding="async"
              />
            </button>
            <figcaption className="step-image-caption">
              <span>Следуйте выделениям на фото</span>
              <button
                type="button"
                className="image-zoom"
                aria-label="Увеличить изображение"
                onClick={() => imageDialogRef.current?.showModal()}
              >
                <Icon name="zoom" size={16} />
                <span>Увеличить</span>
              </button>
            </figcaption>
          </figure>

          <section className="step-read-block card" aria-labelledby="actions-label">
            <h2 id="actions-label" className="read-label">
              Что сделать
            </h2>
            <p className="step-desc">{highlightInstruction(current.description)}</p>
            {current.extra && (
              <p className="step-extra">{highlightInstruction(current.extra)}</p>
            )}
          </section>

          {current.hints?.map((hint, i) => {
            if (hint.type === 'files' && hint.files) {
              return (
                <div key={i} className="file-cards">
                  {hint.files.map((file) => (
                    <div key={file} className="file-chip">
                      <Icon name="file" size={22} />
                      <span className="file-chip-ext">{file}</span>
                    </div>
                  ))}
                </div>
              );
            }
            return (
              <aside key={i} className={`hint hint-${hint.type}`}>
                <Icon
                  name={
                    hint.type === 'warning'
                      ? 'warning'
                      : hint.type === 'tip'
                        ? 'check'
                        : 'info'
                  }
                  size={18}
                />
                <div>{hint.text ? highlightInstruction(hint.text) : null}</div>
              </aside>
            );
          })}

          {current.action && (
            <button
              type="button"
              className="btn btn-secondary step-action"
              onClick={() => onAction(current.action!.url)}
            >
              {current.action.label}
              <Icon name="arrow" size={18} />
            </button>
          )}

          {current.actions && current.actions.length > 0 && (
            <div className="step-actions">
              {current.actions.map((item) => (
                <button
                  key={item.url}
                  type="button"
                  className="btn btn-secondary step-action"
                  onClick={() => {
                    haptic('light');
                    onAction(item.url);
                  }}
                >
                  {item.label}
                  <Icon name="arrow" size={18} />
                </button>
              ))}
            </div>
          )}
        </article>
      </main>

      <footer className="wizard-footer">
        <div className={`wizard-footer-inner${isFirst ? ' wizard-footer-single' : ''}`}>
          {!isFirst && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                haptic('light');
                onBack();
              }}
            >
              <Icon name="back" size={18} />
              Назад
            </button>
          )}
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              haptic(isLast ? 'medium' : 'light');
              onNext();
            }}
          >
            {isLast ? 'Завершить' : 'Далее'}
            <Icon name={isLast ? 'check' : 'arrow'} size={18} />
          </button>
        </div>
      </footer>

      <dialog
        className="image-dialog"
        ref={imageDialogRef}
        aria-label={`Иллюстрация шага ${step}`}
        onClick={(event) => {
          if (event.target === event.currentTarget) imageDialogRef.current?.close();
        }}
      >
        <div className="image-dialog-header">
          <span>
            Шаг {step} · {current.title}
          </span>
          <button
            type="button"
            className="icon-btn"
            aria-label="Закрыть изображение"
            onClick={() => imageDialogRef.current?.close()}
          >
            <Icon name="close" />
          </button>
        </div>
        <div className="image-dialog-scroll">
          <img
            src={current.image}
            alt={`Шаг ${step}: ${current.title}`}
            width="1672"
            height="941"
          />
        </div>
      </dialog>
    </div>
  );
}
