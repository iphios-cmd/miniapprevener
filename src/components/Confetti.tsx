import { useEffect, useRef } from 'react';

type Particle = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  w: number;
  h: number;
  rot: number;
  vr: number;
  color: string;
  life: number;
};

const COLORS = ['#6aa5f4', '#5289e0', '#34c759', '#ff9f0a', '#ff6b6b', '#ffffff', '#a78bfa'];

/** Лёгкий confetti при успешном завершении */
export function Confetti({ active = true }: { active?: boolean }) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!active) return;
    const canvas = ref.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let raf = 0;
    let running = true;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const resize = () => {
      const { innerWidth: w, innerHeight: h } = window;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();

    const w = () => window.innerWidth;
    const h = () => window.innerHeight;
    const particles: Particle[] = [];

    const spawn = (count: number, fromTop = true) => {
      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * w(),
          y: fromTop ? -20 - Math.random() * 80 : h() * 0.35 + Math.random() * 40,
          vx: (Math.random() - 0.5) * 6,
          vy: fromTop ? 2 + Math.random() * 4 : -8 - Math.random() * 6,
          w: 5 + Math.random() * 7,
          h: 8 + Math.random() * 10,
          rot: Math.random() * Math.PI,
          vr: (Math.random() - 0.5) * 0.25,
          color: COLORS[Math.floor(Math.random() * COLORS.length)],
          life: 1,
        });
      }
    };

    spawn(48, false);
    spawn(36, true);

    const burstAt = window.setTimeout(() => spawn(28, false), 280);

    const tick = () => {
      if (!running) return;
      ctx.clearRect(0, 0, w(), h());
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.vy += 0.18;
        p.vx *= 0.995;
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        p.life -= 0.0045;

        if (p.life <= 0 || p.y > h() + 40) {
          particles.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.globalAlpha = Math.max(0, Math.min(1, p.life * 1.2));
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      }

      if (particles.length > 0) {
        raf = requestAnimationFrame(tick);
      } else {
        ctx.clearRect(0, 0, w(), h());
      }
    };

    raf = requestAnimationFrame(tick);
    window.addEventListener('resize', resize);

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      window.clearTimeout(burstAt);
      window.removeEventListener('resize', resize);
    };
  }, [active]);

  if (!active) return null;

  return (
    <canvas
      ref={ref}
      className="confetti-canvas"
      aria-hidden="true"
    />
  );
}
