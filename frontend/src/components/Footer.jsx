export default function Footer({ go }) {
  return (
    <footer>
      <div className="wrap row between foot-row">
        <div className="row" style={{ gap: 10 }}>
          <span className="logo-mark" style={{ width: 22, height: 22, fontSize: 12, borderRadius: 6 }}>P</span>
          PenToText — a context-aware transcription project
        </div>
        <div className="row" style={{ gap: 20 }}>
          <a onClick={() => go('landing')} style={{ cursor: 'pointer' }}>Home</a>
          <a onClick={() => go('auth', 'signup')} style={{ cursor: 'pointer' }}>Create account</a>
        </div>
      </div>
    </footer>
  );
}
