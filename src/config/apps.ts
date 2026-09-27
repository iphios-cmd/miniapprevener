export type AppItem = {
  id: string;
  name: string;
  icon: string;
};

/** Декоративный список приложений — только визуализация, без ссылок и действий */
export const APPS: AppItem[] = [
  { id: 'tbank', name: 'Т-Банк', icon: 'icons/tbank.webp?v=3' },
  { id: 'alfabank', name: 'Альфа-Банк', icon: 'icons/alfabank.webp?v=3' },
  { id: 'sberbank', name: 'СберБанк', icon: 'icons/sberbank.webp?v=3' },
  { id: 'youtube', name: 'YouTube', icon: 'icons/youtube.webp?v=3' },
  { id: 'vk', name: 'ВКонтакте', icon: 'icons/vk.webp?v=3' },
  { id: 'vk-music', name: 'VK Музыка', icon: 'icons/vk-music.webp?v=3' },
  { id: 'vk-video', name: 'VK Видео', icon: 'icons/vk-video.webp?v=3' },
  { id: 'vtb', name: 'ВТБ', icon: 'icons/vtb.webp?v=3' },
  { id: 'yandex-music', name: 'Яндекс Музыка', icon: 'icons/yandex-music.webp?v=3' },
  { id: 'max', name: 'MAX', icon: 'icons/max.webp?v=3' },
  { id: 'rave', name: 'Rave', icon: 'icons/rave.webp?v=3' },
  { id: 'ok', name: 'Одноклассники', icon: 'icons/ok.webp?v=3' },
  { id: 'minecraft', name: 'Minecraft', icon: 'icons/minecraft.webp?v=3' },
  { id: 'nulls-brawl', name: "Null's Brawl", icon: 'icons/nulls-brawl.webp?v=3' },
];
