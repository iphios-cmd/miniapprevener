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
    "image": "images/instruction/step-01.png"
  },
  {
    "id": 2,
    "title": "Получите сертификат",
    "description": "В сообщении от бота нажмите «Получить сертификат». Бот отправит два файла сертификата и пароль для его импорта.",
    "action": {
      "label": "Открыть бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/instruction/step-02.png"
  },
  {
    "id": 3,
    "title": "Установите ESign",
    "description": "В сообщении бота выберите «ESign». На открывшейся странице нажмите «Установить» и дождитесь завершения установки на iPhone.",
    "action": {
      "label": "Открыть бота",
      "url": "https://t.me/revngshop_bot"
    },
    "image": "images/instruction/step-03.png"
  },
  {
    "id": 4,
    "title": "Включите режим разработчика",
    "description": "На iPhone откройте «Настройки» → «Конфиденциальность и безопасность» → «Режим разработчика». Включите режим разработчика.",
    "extra": "Если iPhone предложит перезагрузить устройство, подтвердите перезагрузку. После включения повторно подтвердите активацию режима разработчика.",
    "hints": [
      {
        "type": "info",
        "text": "Название и расположение пункта может немного отличаться в зависимости от версии iOS."
      }
    ],
    "image": "images/instruction/step-04.png"
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
    "image": "images/instruction/step-05.png"
  },
  {
    "id": 6,
    "title": "Откройте импорт в ESign",
    "description": "Откройте ESign и нажмите на три точки «•••» в правом верхнем углу. В появившемся меню выберите «Импорт».",
    "image": "images/instruction/step-06.png"
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
    "image": "images/instruction/step-07.png"
  },
  {
    "id": 8,
    "title": "Импортируйте сертификат",
    "description": "В ESign нажмите на файл .p12 и выберите «Импортировать сертификат». Введите пароль, который бот отправил вместе с сертификатом.",
    "hints": [
      {
        "type": "warning",
        "text": "Не отправляйте пароль от сертификата другим людям."
      }
    ],
    "image": "images/instruction/step-08.png"
  },
  {
    "id": 9,
    "title": "Найдите IPA-файл",
    "description": "Найдите нужное приложение в интернете или Telegram-ботах. Сохраните его IPA-файл в приложение «Файлы», выбрав расположение «На iPhone».",
    "hints": [
      {
        "type": "info",
        "text": "IPA-файл нужно получить самостоятельно. На этом сайте нет ссылок на скачивание."
      }
    ],
    "image": "images/instruction/step-09.png"
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
    "image": "images/instruction/step-10.png"
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
    "image": "images/instruction/step-11.png"
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
    "image": "images/instruction/step-12.png"
  }
];

export const TOTAL_STEPS = STEPS.length;

