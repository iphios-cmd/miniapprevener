import sharp from 'sharp';
import { join } from 'path';

const src = 'c:/Users/9rik/Documents/Codex/2026-09-26/yfg/outputs/ipa-guide-images-v3-unified';
const outDir = 'public/images';

const map = {
  'step-01-open-bot.png': 'step-1-bot.webp',
  'step-02-get-certificate.png': 'step-2-certificate.webp',
  'step-03-install-esign.png': 'step-3-esign.webp',
  'step-04-developer-mode.png': 'step-4-developer-mode.webp',
  'step-05-save-certificates.png': 'step-5-files.webp',
  'step-06-tap-import.png': 'step-6-import.webp',
  'step-08-import-certificate.png': 'step-7-certificate-import.webp',
  'step-09-save-ipa-on-iphone.png': 'step-8-ipa-import.webp',
  'step-10-select-ipa.png': 'step-9-library.webp',
  'step-11-sign-app.png': 'step-10-apps.webp',
  'step-12-install-app.png': 'step-11-sign.webp',
};

for (const [from, to] of Object.entries(map)) {
  const input = join(src, from);
  const output = join(outDir, to);
  await sharp(input).webp({ quality: 90 }).toFile(output);
  console.log(`${from} -> ${to}`);
}

console.log('done');
