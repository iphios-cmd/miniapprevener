/**
 * Download real brand / App Store icons into public/icons/*.webp
 */
import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import sharp from 'sharp';

const OUT = join(process.cwd(), 'public', 'icons');
mkdirSync(OUT, { recursive: true });

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15';

async function get(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': UA, Accept: 'image/*,*/*' },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 200) throw new Error(`small ${buf.length}`);
  return buf;
}

async function itunes(id) {
  for (const country of ['us', 'ru', 'gb']) {
    const meta = await (await fetch(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).json();
    const r = meta.results?.[0];
    if (!r?.artworkUrl512) continue;
    console.log(`  itunes ${id} -> ${r.trackName}`);
    const art = r.artworkUrl512.replace('512x512bb', '1024x1024bb');
    return get(art);
  }
  throw new Error(`itunes miss ${id}`);
}

async function toWebp(buf, name) {
  const out = join(OUT, name);
  await sharp(buf).resize(256, 256, { fit: 'cover' }).webp({ quality: 92 }).toFile(out);
  console.log(`  OK ${name}`);
}

async function logoOnBg(buf, name, bg) {
  const logo = await sharp(buf)
    .resize(170, 170, { fit: 'inside' })
    .png()
    .toBuffer();
  const svg = Buffer.from(
    `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
      <rect width="256" height="256" rx="57" fill="${bg}"/>
    </svg>`,
  );
  const out = join(OUT, name);
  await sharp(svg)
    .composite([{ input: logo, gravity: 'center' }])
    .webp({ quality: 92 })
    .toFile(out);
  console.log(`  OK ${name} (on bg)`);
}

async function tryUrls(urls) {
  let last;
  for (const u of urls) {
    try {
      return await get(u);
    } catch (e) {
      last = e;
      console.log(`  miss ${String(e.message).slice(0, 80)}`);
    }
  }
  throw last || new Error('no urls');
}

const WIKI = (file, size = 250) => {
  const encoded = file
    .split('/')
    .map((part, i, arr) => (i === arr.length - 1 ? encodeURIComponent(part).replace(/%2F/g, '/') : part))
    .join('/');
  const fname = encodeURIComponent(file.split('/').pop());
  return `https://upload.wikimedia.org/wikipedia/commons/thumb/${encoded}/${size}px-${fname}.png`;
};

const jobs = [
  {
    id: 'youtube',
    run: async () => toWebp(await itunes(544007664), 'youtube.webp'),
  },
  {
    id: 'minecraft',
    run: async () => toWebp(await itunes(479516143), 'minecraft.webp'),
  },
  {
    id: 'vk',
    run: async () => {
      const buf = await tryUrls([
        WIKI('f/f3/VK_Compact_Logo_(2021-present).svg'),
        WIKI('2/21/VK.com-logo.svg'),
        'https://vk.com/images/icons/pwa/apple/default.png',
        'https://icon.horse/icon/vk.com',
      ]);
      await logoOnBg(buf, 'vk.webp', '#0077FF');
    },
  },
  {
    id: 'ok',
    run: async () => {
      const buf = await tryUrls([
        WIKI('4/47/OK.ru_logo.svg'),
        'https://icon.horse/icon/ok.ru',
      ]);
      await logoOnBg(buf, 'ok.webp', '#EE8208');
    },
  },
  {
    id: 'sberbank',
    run: async () => {
      const buf = await tryUrls([
        WIKI('a/a4/Sberbank_logo_2020.svg'),
        'https://icon.horse/icon/sber.ru',
        'https://icon.horse/icon/sberbank.ru',
      ]);
      // Sber logo is colorful — white rounded bg looks official
      await logoOnBg(buf, 'sberbank.webp', '#FFFFFF');
    },
  },
  {
    id: 'alfabank',
    run: async () => {
      const buf = await tryUrls([
        WIKI('4/4b/Alfa-Bank_logo.svg'),
        'https://icon.horse/icon/alfabank.ru',
      ]);
      await logoOnBg(buf, 'alfabank.webp', '#EF3124');
    },
  },
  {
    id: 'vtb',
    run: async () => {
      const buf = await tryUrls([
        WIKI('0/0c/VTB_logo.svg', 250),
        WIKI('b/b0/VTB_Bank_logo.svg', 250),
        'https://icon.horse/icon/vtb.ru',
      ]);
      await logoOnBg(buf, 'vtb.webp', '#0055A5');
    },
  },
  {
    id: 'tbank',
    run: async () => {
      // Official-looking brand mark via icon hosts / store search
      try {
        const buf = await itunes(1360253417);
        await toWebp(buf, 'tbank.webp');
        return;
      } catch {}
      const buf = await tryUrls([
        'https://icon.horse/icon/tbank.ru',
        'https://icon.horse/icon/tinkoff.ru',
        'https://www.google.com/s2/favicons?domain=tbank.ru&sz=128',
      ]);
      await logoOnBg(buf, 'tbank.webp', '#FFDD2D');
    },
  },
  {
    id: 'yandex-music',
    run: async () => {
      try {
        await toWebp(await itunes(518133398), 'yandex-music.webp');
        return;
      } catch {}
      const buf = await tryUrls([
        'https://music.yandex.ru/apple-touch-icon.png',
        'https://icon.horse/icon/music.yandex.ru',
      ]);
      await toWebp(buf, 'yandex-music.webp');
    },
  },
  {
    id: 'max',
    run: async () => {
      const buf = await tryUrls([
        'https://max.ru/apple-touch-icon.png',
        'https://web.max.ru/apple-touch-icon.png',
        'https://icon.horse/icon/max.ru',
      ]);
      await toWebp(buf, 'max.webp');
    },
  },
  {
    id: 'rave',
    run: async () => {
      try {
        await toWebp(await itunes(1129958305), 'rave.webp');
        return;
      } catch {}
      const buf = await tryUrls([
        'https://icon.horse/icon/rave.io',
        'https://www.google.com/s2/favicons?domain=rave.io&sz=128',
      ]);
      await logoOnBg(buf, 'rave.webp', '#7B2CBF');
    },
  },
  {
    id: 'vk-music',
    run: async () => {
      // Use official VK Music mark if possible; else VK logo on red
      const buf = await tryUrls([
        WIKI('f/f3/VK_Compact_Logo_(2021-present).svg'),
        'https://vk.com/images/icons/pwa/apple/default.png',
      ]);
      await logoOnBg(buf, 'vk-music.webp', '#FC2C38');
    },
  },
  {
    id: 'vk-video',
    run: async () => {
      const buf = await tryUrls([
        'https://icon.horse/icon/vkvideo.ru',
        WIKI('f/f3/VK_Compact_Logo_(2021-present).svg'),
        'https://vk.com/images/icons/pwa/apple/default.png',
      ]);
      await logoOnBg(buf, 'vk-video.webp', '#2683ED');
    },
  },
  {
    id: 'nulls-brawl',
    run: async () => {
      // Null's Brawl site icon, fallback Brawl Stars store icon for recognition
      try {
        const buf = await tryUrls([
          'https://nulls-brawl.com/apple-touch-icon.png',
          'https://nullsbrawl.com/apple-touch-icon.png',
          'https://nulls-brawl.com/favicon-196x196.png',
          'https://icon.horse/icon/nulls-brawl.com',
        ]);
        await toWebp(buf, 'nulls-brawl.webp');
      } catch {
        await toWebp(await itunes(1229016807), 'nulls-brawl.webp'); // Brawl Stars
      }
    },
  },
];

for (const job of jobs) {
  console.log(`[${job.id}]`);
  try {
    await job.run();
  } catch (e) {
    console.log(`  FAIL ${e.message}`);
  }
}

console.log('done');
