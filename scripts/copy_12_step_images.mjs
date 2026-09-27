import sharp from 'sharp';
import { join } from 'path';

const src = 'c:/Users/9rik/Desktop/Фотки для инструкции';
const outDir = 'public/images';

const map = [
  ['step-01.png', 'step-1-bot.webp'],
  ['step-02.png', 'step-2-certificate.webp'],
  ['step-03.png', 'step-3-esign.webp'],
  ['step-04.png', 'step-4-developer-mode.webp'],
  ['step-05.png', 'step-5-files.webp'],
  ['step-06.png', 'step-6-import.webp'],
  ['step-07.png', 'step-7-certificate-import.webp'],
  ['step-08.png', 'step-8-ipa-import.webp'],
  ['step-09.png', 'step-9-library.webp'],
  ['step-10.png', 'step-10-apps.webp'],
  ['step-11.png', 'step-11-sign.webp'],
  ['step-12.jpg', 'step-12-install.webp'],
];

for (const [from, to] of map) {
  await sharp(join(src, from)).webp({ quality: 90 }).toFile(join(outDir, to));
  console.log(`${from} -> ${to}`);
}

console.log('done');
