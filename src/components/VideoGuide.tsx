import { useRef, useState } from 'react';
import { VIDEO_URL } from '../config/steps';

type Props = {
  haptic: (style?: 'light' | 'medium' | 'heavy') => void;
};

export function VideoGuide({ haptic }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggle = () => {
    const el = videoRef.current;
    if (!el) return;
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

      <div className={`video-card${playing ? ' is-playing' : ''}`}>
        <video
          ref={videoRef}
          className="video-player"
          src={VIDEO_URL}
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
      </div>
    </section>
  );
}
