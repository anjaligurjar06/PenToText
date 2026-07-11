import { ScanLine } from 'lucide-react';

export function squigglePath(width, seed = 0) {
  const segs = Math.max(4, Math.round(width / 16));
  let d = `M0,${9 + Math.sin(seed) * 2}`;
  for (let i = 1; i <= segs; i++) {
    const x = (width / segs) * i;
    const y = 9 + Math.sin(i * 1.7 + seed) * 5;
    const cx = x - (width / segs) / 2;
    const cy = y + (i % 2 ? 5 : -5);
    d += ` Q${cx},${cy} ${x},${y}`;
  }
  return d;
}

export function SquiggleLine({ width, seed = 0, color = 'var(--ink-soft)', h = 16 }) {
  return (
    <svg viewBox={`0 0 ${width} 18`} width={width} height={h} style={{ display: 'block' }}>
      <path d={squigglePath(width, seed)} stroke={color} strokeWidth="2.2" fill="none" strokeLinecap="round" />
    </svg>
  );
}

/** Stylized mock of a scanned handwritten page — used on the Review page. */
export function PageMock({ variant = 'prescription' }) {
  const lineWidths = variant === 'prescription'
    ? [120, 210, 180, 240, 90, 200, 160, 220, 100]
    : [200, 230, 90, 210, 190, 240, 130, 200, 170, 110];
  return (
    <div className="col" style={{ gap: 14, height: '100%' }}>
      <div className="row between" style={{ marginBottom: 4 }}>
        <div className="script" style={{ fontSize: 22, color: 'var(--indigo)' }}>
          {variant === 'prescription' ? 'Dr. M. Reyes, MD' : 'Exam Script — Booklet A'}
        </div>
        <ScanLine size={18} color="var(--ink-faint)" />
      </div>
      <hr className="divider" />
      <div className="col" style={{ gap: 16, marginTop: 6 }}>
        {lineWidths.map((w, i) => (
          <SquiggleLine key={i} width={w} seed={i * 1.3} />
        ))}
      </div>
    </div>
  );
}

/** Handwriting-to-type hero demo — the landing page's signature visual. */
export function HeroDemo() {
  return (
    <div className="demo-card">
      <div className="demo-tape" />
      <div className="demo-label">handwritten input</div>
      <div className="demo-scrawl">Amoxicillin 500mg — 3x daily, 7 days</div>
      <div className="demo-arrow-wrap">
        <svg width="150" height="34" viewBox="0 0 150 34">
          <path className="draw-in" d="M8,6 C 40,32 100,32 138,10" stroke="var(--marigold-line)" strokeWidth="2.4" fill="none" strokeLinecap="round" />
          <polygon points="132,4 142,10 130,16" fill="var(--marigold-line)" />
        </svg>
      </div>
      <div className="demo-label">typed output · context: dermatology</div>
      <div className="demo-typed">
        <span className="flag">Amoxicillin</span> 500&nbsp;mg — three times daily for seven days
      </div>
    </div>
  );
}

/** Labeled form field wrapper. */
export function Field({ label, children }) {
  return (
    <div>
      <label className="field-label">{label}</label>
      {children}
    </div>
  );
}
