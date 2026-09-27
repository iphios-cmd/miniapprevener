import { useState, type ReactNode } from 'react';
import { SUPPORT_URL } from '../config/steps';

type Props = {
  onSupport: (url: string) => void;
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

type Problem = {
  id: string;
  title: string;
  content: ReactNode;
};

const PROBLEMS: Problem[] = [
  {
    id: 'install',
    title: 'Приложение не устанавливается',
    content: (
      <ul className="faq-list">
        <li>Убедитесь, что сертификат действителен</li>
        <li>Проверьте, что импортированы файлы .p12 и .mobileprovision</li>
        <li>Убедитесь, что включён режим разработчика</li>
        <li>Попробуйте повторно подписать приложение</li>
        <li>Проверьте наличие свободного места на iPhone</li>
        <li>При необходимости обратитесь в поддержку</li>
      </ul>
    ),
  },
  {
    id: 'open',
    title: 'Приложение перестало открываться',
    content: (
      <p>
        Возможно, срок действия сертификата закончился или сертификат был отозван.
        Получите действующий сертификат и повторно подпишите IPA-файл.
      </p>
    ),
  },
  {
    id: 'password',
    title: 'ESign запрашивает пароль',
    content: (
      <p>
        Используйте пароль, который был предоставлен вместе с вашим сертификатом. Не
        вводите пароль от Apple ID или Telegram.
      </p>
    ),
  },
  {
    id: 'help',
    title: 'Нужна помощь',
    content: null,
  },
];

export function FAQ({ onSupport, haptic }: Props) {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <section className="card faq-card">
      <h2 className="faq-title">Проблемы</h2>
      <div className="faq-list-wrap">
        {PROBLEMS.map((item) => {
          const open = openId === item.id;
          return (
            <div key={item.id} className={`faq-item${open ? ' open' : ''}`}>
              <button
                type="button"
                className="faq-trigger"
                aria-expanded={open}
                onClick={() => {
                  haptic('light');
                  setOpenId(open ? null : item.id);
                }}
              >
                <span>{item.title}</span>
                <span className="faq-chevron-wrap" aria-hidden="true">
                  <svg className="faq-chevron" viewBox="0 0 24 24" width="18" height="18">
                    <path
                      fill="currentColor"
                      d="M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6z"
                    />
                  </svg>
                </span>
              </button>
              <div className="faq-panel" aria-hidden={!open}>
                <div className="faq-body">
                  {item.id === 'help' ? (
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => onSupport(SUPPORT_URL)}
                    >
                      Тех. Поддержка
                    </button>
                  ) : (
                    item.content
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
