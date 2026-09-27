type Props = {
  name:
    | 'arrow'
    | 'back'
    | 'home'
    | 'clock'
    | 'check'
    | 'file'
    | 'info'
    | 'warning'
    | 'zoom'
    | 'close'
    | 'apps'
    | 'guide';
  size?: number;
  className?: string;
};

const paths = {
  arrow: 'M5 12h14m-6-6 6 6-6 6',
  back: 'M19 12H5m6-6-6 6 6 6',
  home: 'm3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z',
  clock: 'M12 8v5l3 2',
  check: 'm5 12 4 4L19 6',
  file: 'M14 2H5a1 1 0 0 0-1 1v18a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V8Zm0 0v6h6M8 13h8M8 17h5',
  info: 'M12 11v6m0-10h.01',
  warning: 'M12 8v5m0 4h.01M10.3 3.7 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.7a2 2 0 0 0-3.4 0Z',
  zoom: 'm16 16 5 5M10 7v6m-3-3h6',
  close: 'm6 6 12 12M6 18 18 6',
  apps: '',
  guide: '',
};

export function Icon({ name, size = 20, className }: Props) {
  if (name === 'apps') {
    return (
      <svg
        className={className}
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
      >
        <rect x="3" y="3" width="8" height="8" rx="2" />
        <rect x="13" y="3" width="8" height="8" rx="2" />
        <rect x="3" y="13" width="8" height="8" rx="2" />
        <rect x="13" y="13" width="8" height="8" rx="2" />
      </svg>
    );
  }

  if (name === 'guide') {
    return (
      <svg
        className={className}
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
      >
        <path d="M7 2.75A2.25 2.25 0 0 0 4.75 5v14A2.25 2.25 0 0 0 7 21.25h10A2.25 2.25 0 0 0 19.25 19V5A2.25 2.25 0 0 0 17 2.75H7Z" opacity="0.28" />
        <circle cx="8.15" cy="8.15" r="1.25" />
        <rect x="11" y="7.35" width="6.5" height="1.6" rx="0.8" />
        <circle cx="8.15" cy="12.15" r="1.25" />
        <rect x="11" y="11.35" width="6.5" height="1.6" rx="0.8" />
        <circle cx="8.15" cy="16.15" r="1.25" />
        <rect x="11" y="15.35" width="4.8" height="1.6" rx="0.8" />
      </svg>
    );
  }

  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {(name === 'clock' || name === 'info') && <circle cx="12" cy="12" r="9" />}
      {name === 'zoom' && <circle cx="10" cy="10" r="7" />}
      <path d={paths[name]} />
    </svg>
  );
}

