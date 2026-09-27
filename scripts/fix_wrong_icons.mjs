import { join } from 'node:path';
import sharp from 'sharp';

const OUT = join(process.cwd(), 'public', 'icons');

async function get(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0', Accept: 'image/*,*/*' },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 400) throw new Error('small');
  return buf;
}

async function itunes(id, country = 'us') {
  const meta = await (await fetch(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).json();
  const r = meta.results?.[0];
  if (!r) throw new Error(`no result ${id}`);
  console.log(`itunes ${id} -> ${r.trackName}`);
  return get(r.artworkUrl512.replace('512x512bb', '1024x1024bb'));
}

async function itunesSearch(term, country = 'ru') {
  const qs = new URLSearchParams({ term, country, entity: 'software', limit: '8' });
  const meta = await (await fetch(`https://itunes.apple.com/search?${qs}`)).json();
  for (const r of meta.results || []) {
    console.log(`  candidate: ${r.trackName} (${r.bundleId})`);
  }
  const r = (meta.results || []).find((x) =>
    /yandex music|яндекс музыка|max|rave|brawl stars|tinkoff|т-банк|alfa|альфа|vtb|втб/i.test(
      `${x.trackName} ${x.bundleId}`,
    ),
  ) || meta.results?.[0];
  if (!r) throw new Error('search miss');
  console.log(`picked ${r.trackName}`);
  return get(r.artworkUrl512.replace('512x512bb', '1024x1024bb'));
}

async function save(buf, name) {
  await sharp(buf).resize(256, 256, { fit: 'cover' }).webp({ quality: 93 }).toFile(join(OUT, name));
  console.log('saved', name);
}

async function logoOnBg(buf, name, bg) {
  const logo = await sharp(buf, { density: 300 })
    .resize(168, 168, { fit: 'inside' })
    .png()
    .toBuffer();
  const svg = Buffer.from(
    `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg"><rect width="256" height="256" rx="57" fill="${bg}"/></svg>`,
  );
  await sharp(svg)
    .composite([{ input: logo, gravity: 'center' }])
    .webp({ quality: 93 })
    .toFile(join(OUT, name));
  console.log('saved', name);
}

// Fix critical wrong icons
const fixes = [
  async () => {
    console.log('[yandex-music]');
    await save(await itunes(518133398), 'yandex-music.webp');
  },
  async () => {
    console.log('[max]');
    // Try search for official MAX messenger
    try {
      await save(await itunesSearch('MAX мессенджер', 'ru'), 'max.webp');
    } catch {
      await save(await itunesSearch('MAX', 'ru'), 'max.webp');
    }
  },
  async () => {
    console.log('[nulls-brawl] use Brawl Stars official icon');
    await save(await itunes(1229016807), 'nulls-brawl.webp');
  },
  async () => {
    console.log('[rave]');
    try {
      await save(await itunes(1129958305), 'rave.webp');
    } catch {
      await save(await itunesSearch('Rave Watch Together', 'us'), 'rave.webp');
    }
  },
  async () => {
    console.log('[minecraft] HD');
    await save(await itunes(479516143, 'us'), 'minecraft.webp');
  },
  async () => {
    console.log('[tbank] clearbit');
    try {
      await logoOnBg(await get('https://logo.clearbit.com/tbank.ru'), 'tbank.webp', '#FFDD2D');
    } catch {
      await logoOnBg(await get('https://logo.clearbit.com/tinkoff.ru'), 'tbank.webp', '#FFDD2D');
    }
  },
  async () => {
    console.log('[alfabank] clearbit');
    await logoOnBg(await get('https://logo.clearbit.com/alfabank.ru'), 'alfabank.webp', '#EF3124');
  },
  async () => {
    console.log('[vtb] clearbit');
    await logoOnBg(await get('https://logo.clearbit.com/vtb.ru'), 'vtb.webp', '#0055A5');
  },
];

for (const fn of fixes) {
  try {
    await fn();
  } catch (e) {
    console.log('FAIL', e.message);
  }
}
