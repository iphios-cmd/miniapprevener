import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import sharp from 'sharp';

const OUT = join(process.cwd(), 'public', 'icons');
const UA = 'Mozilla/5.0';

async function get(url) {
  const res = await fetch(url, { headers: { 'User-Agent': UA }, redirect: 'follow' });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  return Buffer.from(await res.arrayBuffer());
}

async function logoOnBg(buf, name, bg) {
  // sharp may need density for ico; try png conversion first
  let logoBuf;
  try {
    logoBuf = await sharp(buf, { density: 300 }).resize(170, 170, { fit: 'inside' }).png().toBuffer();
  } catch {
    // fallback: write temp and retry as raw
    logoBuf = await sharp(buf).resize(170, 170, { fit: 'inside' }).png().toBuffer();
  }
  const svg = Buffer.from(
    `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg"><rect width="256" height="256" rx="57" fill="${bg}"/></svg>`,
  );
  await sharp(svg)
    .composite([{ input: logoBuf, gravity: 'center' }])
    .webp({ quality: 92 })
    .toFile(join(OUT, name));
  console.log('OK', name);
}

async function square(buf, name) {
  await sharp(buf).resize(256, 256, { fit: 'cover' }).webp({ quality: 92 }).toFile(join(OUT, name));
  console.log('OK', name);
}

const fixes = [
  {
    name: 'tbank.webp',
    bg: '#FFDD2D',
    urls: [
      'https://www.google.com/s2/favicons?domain=tbank.ru&sz=128',
      'https://icons.duckduckgo.com/ip3/tbank.ru.ico',
      'https://logo.clearbit.com/tbank.ru',
      'https://logo.clearbit.com/tinkoff.ru',
    ],
  },
  {
    name: 'alfabank.webp',
    bg: '#EF3124',
    urls: [
      'https://www.google.com/s2/favicons?domain=alfabank.ru&sz=128',
      'https://icons.duckduckgo.com/ip3/alfabank.ru.ico',
      'https://logo.clearbit.com/alfabank.ru',
    ],
  },
  {
    name: 'vtb.webp',
    bg: '#0055A5',
    urls: [
      'https://www.google.com/s2/favicons?domain=vtb.ru&sz=128',
      'https://icons.duckduckgo.com/ip3/vtb.ru.ico',
      'https://logo.clearbit.com/vtb.ru',
    ],
  },
];

for (const job of fixes) {
  console.log(job.name);
  let ok = false;
  for (const url of job.urls) {
    try {
      const buf = await get(url);
      if (job.bg) await logoOnBg(buf, job.name, job.bg);
      else await square(buf, job.name);
      ok = true;
      console.log('  from', url.slice(0, 70));
      break;
    } catch (e) {
      console.log('  miss', e.message.slice(0, 90));
    }
  }
  if (!ok) console.log('  FAIL');
}
