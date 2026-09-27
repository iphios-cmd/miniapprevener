export type StepAction = { label: string; url: string };
export type StepHint = {
  type: 'tip' | 'warning' | 'info' | 'files';
  text?: string;
  files?: string[];
};
export type InstructionStep = {
  id: number;
  title: string;
  description: string;
  image: string;
  extra?: string;
  hints?: StepHint[];
  action?: StepAction;
  actions?: StepAction[];
};

export const BOT_URL = 'https://t.me/revngshop_bot';
export const BOT_USERNAME = '@revngshop_bot';
export const SUPPORT_URL = 'https://t.me/RevengSupportBot';
export const SUPPORT_USERNAME = '@RevengSupportBot';

/** Положите файл сюда: public/video/instruction.mp4 */
export const VIDEO_URL = 'video/instruction.mp4';
export const VIDEO_POSTER = 'video/poster.jpg';

// Порядок и подписи соответствуют обновлённой серии из 12 изображений.
export const STEPS: InstructionStep[] = [
  {
    "id": 1,
    "title": "Откройте Telegram-бота",
    "description": "Зайдите в Telegram-бота @revngshop_bot и найдите сообщение о готовности вашего сертификата.",
    "action": {
      "label": "Перейти в бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/step-1-bot.webp?v=7"
  },
  {
    "id": 2,
    "title": "Получите сертификат",
    "description": "В сообщении от бота нажмите «Получить сертификат». Бот отправит два файла сертификата и пароль для его импорта.",
    "action": {
      "label": "Открыть бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/step-2-certificate.webp?v=7"
  },
  {
    "id": 3,
    "title": "Установите ESign",
    "description": "В сообщении бота выберите «ESign». На открывшейся странице нажмите «Установить» и дождитесь завершения установки на iPhone.",
    "action": {
      "label": "Открыть бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/step-3-esign.webp?v=7"
  },
  {
    "id": 4,
    "title": "Включите режим разработчика",
    "description": "На iPhone откройте «Настройки» → «Конфиденциальность и безопасность» → «Режим разработчика». Включите режим разработчика.",
    "extra": "Если не появился режим разработчика, то перезагрузите устройство и попробуйте еще раз",
    "image": "images/step-4-developer-mode.webp?v=7"
  },
  {
    "id": 5,
    "title": "Сохраните файлы сертификата",
    "description": "Вернитесь в @revngshop_bot. Сохраните оба полученных файла — .p12 и .mobileprovision — в приложение «Файлы» на iPhone.",
    "hints": [
      {
        "type": "files",
        "files": [
          ".p12",
          ".mobileprovision"
        ]
      }
    ],
    "action": {
      "label": "Перейти в бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/step-5-files.webp?v=7"
  },
  {
    "id": 6,
    "title": "Откройте импорт в ESign",
    "description": "Откройте ESign и нажмите на три точки «•••» в правом верхнем углу. В появившемся меню выберите «Импорт».",
    "image": "images/step-6-import.webp?v=7"
  },
  {
    "id": 7,
    "title": "Выберите файлы сертификата",
    "description": "В открывшемся приложении «Файлы» найдите сохранённые .p12 и .mobileprovision. Импортируйте их в ESign по очереди.",
    "hints": [
      {
        "type": "tip",
        "text": "Повторите импорт для второго файла. Оба файла должны появиться внутри ESign."
      }
    ],
    "image": "images/step-7-certificate-import.webp?v=7"
  },
  {
    "id": 8,
    "title": "Импортируйте сертификат",
    "description": "В ESign нажмите на файл .p12 и выберите «Импортировать сертификат». Введите пароль, который бот отправил вместе с сертификатом.",
    "image": "images/step-8-ipa-import.webp?v=7"
  },
  {
    "id": 9,
    "title": "Найдите IPA-файл",
    "description": "Найдите нужное приложение в канале или IPA-библиотеке. Сохраните его IPA-файл в приложение «Файлы», выбрав расположение «На iPhone».",
    "extra": "Канал, где вы можете найти нужные приложения",
    "actions": [
      {
        "label": "Канал revenger.ios",
        "url": "https://t.me/+U1Z6KRwWCsE4MTEy"
      },
      {
        "label": "IPA библиотека",
        "url": "https://t.me/appstoreipabot"
      }
    ],
    "image": "images/step-9-library.webp?v=7"
  },
  {
    "id": 10,
    "title": "Добавьте IPA в ESign",
    "description": "В ESign через «•••» → «Импорт» выберите сохранённый .ipa-файл. Затем нажмите на него и выберите «Импортировать в библиотеку приложений».",
    "hints": [
      {
        "type": "tip",
        "text": "После импорта приложение появится во внутренней библиотеке ESign."
      }
    ],
    "image": "images/step-10-apps.webp?v=7"
  },
  {
    "id": 11,
    "title": "Подпишите приложение",
    "description": "Откройте вкладку «Приложения» в нижнем меню ESign. Выберите нужное приложение и нажмите «Подписать». Дождитесь окончания подписи.",
    "hints": [
      {
        "type": "tip",
        "text": "Не закрывайте ESign до завершения процесса подписи."
      }
    ],
    "image": "images/step-11-sign.webp?v=7"
  },
  {
    "id": 12,
    "title": "Установите приложение",
    "description": "После окончания подписи нажмите «Установить». Подтвердите установку в системном окне и дождитесь её завершения.",
    "hints": [
      {
        "type": "tip",
        "text": "Приложение должно появиться на главном экране вашего iPhone."
      }
    ],
    "image": "images/step-12-install.webp?v=7"
  }
];

export const TOTAL_STEPS = STEPS.length;

