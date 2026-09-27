# Инструкция по установке IPA — Telegram Mini App

Современный адаптивный Telegram Mini App на русском языке: пошаговая установка IPA на iPhone через личный сертификат разработчика и ESign.

## Стек

- React 19 + TypeScript
- Vite
- Telegram WebApp API (`telegram-web-app.js`)
- localStorage для прогресса

## Быстрый старт

```bash
npm install
npm run dev
```

Откройте адрес из терминала (обычно `http://localhost:5173`) в браузере или через [Telegram WebApp](https://core.telegram.org/bots/webapps) / туннель (ngrok, Cloudflare Tunnel).

## Сборка

```bash
npm run build
```

Готовые файлы появятся в папке `dist/`. Разместите их на HTTPS-хостинге и укажите URL в настройках бота (`BotFather` → Menu Button / Web App).

Проверка production-сборки локально:

```bash
npm run preview
```

## Telegram Mini App

В `index.html` подключен SDK:

```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

При запуске приложение вызывает:

- `Telegram.WebApp.ready()`
- `Telegram.WebApp.expand()`
- определение светлой / тёмной темы
- `HapticFeedback` на основных кнопках
- `openTelegramLink()` для перехода в `@revngshop_bot`

Для корректной работы внутри Telegram нужен HTTPS-URL и привязка к боту.

## Структура проекта

```
src/
  config/
    apps.ts      # декоративные иконки приложений
    steps.ts     # 11 шагов инструкции + картинки
  components/    # UI экранов
  hooks/         # Telegram SDK и прогресс
  lib/storage.ts # localStorage
public/
  images/        # скриншоты шагов (*.webp)
  icons/         # иконки приложений
  logo.png
```

## Замена изображений

Пути к картинкам шагов задаются в `src/config/steps.ts`:

```ts
image: '/images/step-1-bot.webp'
```

Замените файлы в `public/images/` своими скриншотами с теми же именами — менять код не нужно.

Иконки приложений — в `src/config/apps.ts` и папке `public/icons/`. Сейчас стоят качественные заглушки; их можно заменить на `.webp` и обновить поле `icon`.

## Экраны

1. Главная — логотип, заголовок, сетка приложений (некликабельная), кнопка «Начать устанавливать», FAQ
2. Предупреждение о рисках (чекбокс обязателен)
3. Пошаговый мастер (11 шагов)
4. Экран успешного завершения
5. Возобновление прогресса при повторном открытии

## Безопасность

Сайт **не** принимает и **не** загружает сертификаты, пароли и IPA пользователя. Все действия выполняются локально на устройстве. Прямых ссылок на IPA нет.

## Адаптив

Верстка рассчитана на ширину от 320 px, с учётом `safe-area-inset` для iPhone и Telegram.
