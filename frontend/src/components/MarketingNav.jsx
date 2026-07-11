export default function MarketingNav({ go }) {
  return (
    <div className="mnav">
      <div className="wrap row between mnav-inner">
        <a className="logo" onClick={() => go('landing')} style={{ cursor: 'pointer' }}>
          <span className="logo-mark">P</span> PenToText
        </a>
        <div className="mnav-links">
          <a href="#how">How it works</a>
          <a href="#categories">Document types</a>
          <a href="#trust">Privacy</a>
        </div>
        <div className="row" style={{ gap: 10 }}>
          <button className="btn btn-ghost" onClick={() => go('auth', 'login')}>Log in</button>
          <button className="btn btn-primary" onClick={() => go('auth', 'signup')}>Get started</button>
        </div>
      </div>
    </div>
  );
}
