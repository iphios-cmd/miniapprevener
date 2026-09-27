import type { ReactNode } from 'react';

type Props = {
  screen: string;
  children: ReactNode;
};

export function ScreenTransition({ screen, children }: Props) {
  return (
    <div key={screen} className="screen-transition" data-screen={screen}>
      {children}
    </div>
  );
}
