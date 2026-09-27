import { useEffect, useRef, useState } from 'react';
import { VIDEO_POSTER, VIDEO_URL } from '../config/steps';

type Props = {
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

export function VideoGuide({ haptic }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [ready, setReady] = useState(false);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch(VIDEO_URL, { method: 'HEAD' })
      .then((res) => {
        if (!cancelled) setReady(res.ok);
      })
      .catch(() => {
        if (!cancelled) setReady(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const toggle = () => {
    const el = videoRef.current;
    if (!el || !ready) return;
    haptic('light');
    if (el.paused) {
      void el.play();
    } else {
      el.pause();
    }
  };

  return (
    <section className="video-guide" aria-labelledby="video-guide-title">
      <div className="video-guide-head">
        <h2 id="video-guide-title" className="video-guide-title">
          Видеоинструкция
        </h2>
        <p className="video-guide-sub">Коротко покажем весь процесс</p>
      </div>

      <div className={`video-card${ready ? '' : ' is-empty'}${playing ? ' is-playing' : ''}`}>
        {ready ? (
          <>
            <video
              ref={videoRef}
              className="video-player"
              src={VIDEO_URL}
              poster={VIDEO_POSTER}
              playsInline
              preload="metadata"
              controls={playing}
              onPlay={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              onEnded={() => setPlaying(false)}
            />
            {!playing && (
              <button
                type="button"
                className="video-play"
                aria-label="Смотреть видеоинструкцию"
                onClick={toggle}
              >
                <span className="video-play-icon" aria-hidden="true" />
              </button>
            )}
          </>
        ) : (
          <div className="video-placeholder">
            <span className="video-play-icon" aria-hidden="true" />
            <span className="video-placeholder-text">Видео скоро появится</span>
          </div>
        )}
      </div>
    </section>
  );
}
