type Props = {
  open: boolean;
  step: number;
  onContinue: () => void;
  onRestart: () => void;
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

export function ResumeModal({ open, step, onContinue, onRestart, haptic }: Props) {
  if (!open) return null;

  return (
    <div className="modal-overlay open" role="dialog" aria-modal="true" aria-labelledby="resume-title">
      <div className="modal">
        <div className="modal-handle" />
        <h2 id="resume-title" className="modal-title">
          Продолжить с шага {step}?
        </h2>
        <p className="modal-sub">
          Вы уже начали инструкцию. Можно продолжить с того места, где остановились, или
          начать заново.
        </p>
        <div className="modal-actions">
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              haptic('medium');
              onContinue();
            }}
          >
            Продолжить
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => {
              haptic('light');
              onRestart();
            }}
          >
            Начать заново
          </button>
        </div>
      </div>
    </div>
  );
}
