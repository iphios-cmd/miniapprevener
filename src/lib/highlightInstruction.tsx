import type { ReactNode } from 'react';

/** Выделяет в тексте кнопки «…», файлы .ext, @ботов и пункты меню */
export function highlightInstruction(text: string): ReactNode[] {
  const pattern =
    /(«[^»]+»|"[^"]+"|@[a-zA-Z0-9_]+|\.(?:p12|mobileprovision|ipa)\b|\bESign\b|\bIPA\b|→)/g;

  const parts = text.split(pattern);

  return parts.map((part, i) => {
    if (!part) return null;

    if (part.startsWith('«') && part.endsWith('»')) {
      return (
        <mark key={i} className="hl hl-action">
          {part.slice(1, -1)}
        </mark>
      );
    }

    if (part.startsWith('"') && part.endsWith('"')) {
      return (
        <mark key={i} className="hl hl-action">
          {part.slice(1, -1)}
        </mark>
      );
    }

    if (part.startsWith('@')) {
      return (
        <mark key={i} className="hl hl-bot">
          {part}
        </mark>
      );
    }

    if (/^\.(p12|mobileprovision|ipa)$/i.test(part)) {
      return (
        <mark key={i} className="hl hl-file">
          {part}
        </mark>
      );
    }

    if (part === '→') {
      return (
        <span key={i} className="hl-arrow">
          →
        </span>
      );
    }

    if (part === 'ESign' || part === 'IPA') {
      return <strong key={i} className="hl hl-app">{part}</strong>;
    }

    return <span key={i}>{part}</span>;
  });
}
