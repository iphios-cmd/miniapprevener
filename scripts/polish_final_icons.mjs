import { join } from 'node:path';
import sharp from 'sharp';

const OUT = join(process.cwd(), 'public', 'icons');

async function get(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0', Accept: '*/*' },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 300) throw new Error('small');
  // ensure image
  await sharp(buf).metadata();
  return buf;
}

async function save(buf, name) {
  await sharp(buf).resize(256, 256, { fit: 'cover' }).webp({ quality: 93 }).toFile(join(OUT, name));
  console.log('OK', name);
}

async function logoOnBg(buf, name, bg) {
  const logo = await sharp(buf, { density: 300 }).resize(160, 160, { fit: 'inside' }).png().toBuffer();
  const svg = Buffer.from(
    `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg"><rect width="256" height="256" rx="57" fill="${bg}"/></svg>`,
  );
  await sharp(svg).composite([{ input: logo, gravity: 'center' }]).webp({ quality: 93 }).toFile(join(OUT, name));
  console.log('OK', name);
}

async function textIcon(name, text, bg, fg = '#fff', fontSize = 72) {
  const svg = Buffer.from(`<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="57" fill="${bg}"/>
    <text x="128" y="145" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-size="${fontSize}" font-weight="800" fill="${fg}">${text}</text>
  </svg>`);
  await sharp(svg).webp({ quality: 93 }).toFile(join(OUT, name));
  console.log('OK', name, '(wordmark)');
}

// Restore Rave
console.log('[rave]');
try {
  await logoOnBg(await get('https://icon.horse/icon/rave.io'), 'rave.webp', '#8032CF');
} catch (e) {
  console.log('rave fail', e.message);
  // recreate approximate official wordmark icon
  const svg = Buffer.from(`<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="57" fill="#8032CF"/>
    <circle cx="128" cy="128" r="70" fill="#111"/>
    <text x="128" y="140" text-anchor="middle" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="#fff">rave</text>
  </svg>`);
  await sharp(svg).webp({ quality: 93 }).toFile(join(OUT, 'rave.webp'));
  console.log('OK rave.webp (brand wordmark)');
}

// Yandex Music via search
console.log('[yandex-music]');
try {
  const qs = new URLSearchParams({ term: 'Яндекс Музыка', country: 'ru', entity: 'software', limit: '10' });
  const meta = await (await fetch(`https://itunes.apple.com/search?${qs}`)).json();
  const r = (meta.results || []).find((x) => /music|музык/i.test(x.trackName) && /yandex|яндекс/i.test(x.trackName + x.bundleId));
  console.log('candidates', (meta.results || []).slice(0, 5).map((x) => x.trackName));
  if (r) {
    await save(await get(r.artworkUrl512.replace('512x512bb', '1024x1024bb')), 'yandex-music.webp');
  } else {
    await logoOnBg(await get('https://icon.horse/icon/music.yandex.ru'), 'yandex-music.webp', '#111111');
  }
} catch (e) {
  console.log('ym fail', e.message);
  try {
    await logoOnBg(await get('https://www.google.com/s2/favicons?domain=music.yandex.ru&sz=128'), 'yandex-music.webp', '#FFCC00');
  } catch (e2) {
    console.log(e2.message);
  }
}

// VTB official wordmark (favicon was wrong)
console.log('[vtb]');
await textIcon('vtb.webp', 'ВТБ', '#0055A5', '#ffffff', 78);

// MAX - keep MaxMessenger if good, else recreate purple MAX
console.log('[max] verify');
try {
  const qs = new URLSearchParams({ term: 'MaxMessenger', country: 'ru', entity: 'software', limit: '5' });
  const meta = await (await fetch(`https://itunes.apple.com/search?${qs}`)).json();
  const r = (meta.results || []).find((x) => x.bundleId === 'me.max.messenger') || meta.results?.[0];
  if (r) {
    console.log('using', r.trackName, r.bundleId);
    await save(await get(r.artworkUrl512.replace('512x512bb', '1024x1024bb')), 'max.webp');
  }
} catch (e) {
  console.log(e.message);
}

// VK Music - red official style with white note using VK logo
console.log('[vk-music]');
try {
  await logoOnBg(await get('https://vk.com/images/icons/pwa/apple/default.png'), 'vk-music.webp', '#FC2C38');
} catch (e) {
  console.log(e.message);
}

console.log('done');
