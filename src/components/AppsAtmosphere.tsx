import { APPS } from '../config/apps';

export function AppsAtmosphere() {
  return (
    <section className="apps-showcase apple-enter" aria-labelledby="apps-title">
      <div className="apps-showcase-heading">
        <span className="eyebrow">На вашем iPhone</span>
        <h2 id="apps-title">Знакомые приложения.</h2>
        <p>Банки, музыка, видео и игры</p>
      </div>
      <ul className="apps-grid">
        {APPS.map((app) => (
          <li className="app-tile" key={app.id} title={app.name}>
            <div className="app-icon app-icon-img">
              <img src={app.icon} alt="" width="64" height="64" decoding="async" draggable={false} />
            </div>
            <span className="app-name">{app.name}</span>
          </li>
        ))}
      </ul>
      <div className="apps-showcase-caption">
        <span className="showcase-dot" aria-hidden="true" />
        Всё начинается с одной инструкции
      </div>
    </section>
  );
}

