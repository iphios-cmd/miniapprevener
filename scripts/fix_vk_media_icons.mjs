import { join } from 'node:path';
import sharp from 'sharp';

const OUT = join(process.cwd(), 'public', 'icons');

async function writeSvg(name, svg) {
  await sharp(Buffer.from(svg)).webp({ quality: 93 }).toFile(join(OUT, name));
  console.log('OK', name);
}

// Official-looking VK Music (red + white glyph + note)
await writeSvg(
  'vk-music.webp',
  `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" rx="57" fill="#FC2C38"/>
  <text x="128" y="118" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-size="64" font-weight="800" fill="#fff">VK</text>
  <g fill="#fff" transform="translate(88 145)">
    <circle cx="16" cy="36" r="14"/>
    <circle cx="58" cy="28" r="14"/>
    <rect x="26" y="0" width="8" height="36"/>
    <rect x="68" y="-8" width="8" height="36"/>
    <path d="M34 0 L76 -8 L76 2 L34 10 Z"/>
  </g>
</svg>`,
);

// Official-looking VK Video
await writeSvg(
  'vk-video.webp',
  `<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" rx="57" fill="#2683ED"/>
  <text x="128" y="108" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-size="52" font-weight="800" fill="#fff">VK</text>
  <rect x="68" y="128" width="120" height="72" rx="18" fill="#fff"/>
  <polygon points="112,146 112,182 148,164" fill="#2683ED"/>
</svg>`,
);

console.log('done');
