import { Plus, FileText, ChevronRight } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { HISTORY_DOCS } from '../data.js';

export default function Dashboard({ go }) {
  const recent = HISTORY_DOCS.slice(0, 4);
  return (
    <AppShell view="dashboard" go={go}>
      <div className="topbar">
        <div className="page-title serif">Good afternoon, Jordan</div>
        <div className="page-sub">Here's what's happened since your last visit.</div>
      </div>

      <div className="stat-grid">
        <div className="card stat-card">
          <span className="lbl">Documents</span>
          <b>24</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>transcribed total</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">This month</span>
          <b>7</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>+3 vs last month</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">Avg. confidence</span>
          <b>91%</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>across all documents</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">Needs review</span>
          <b>2</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>flagged words open</span>
        </div>
      </div>

      <div className="card" style={{ padding: '22px 22px 26px', marginBottom: 24, background: 'var(--indigo-deep)', color: '#fff', border: 'none' }}>
        <div className="row between">
          <div>
            <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>Have a new document to read?</div>
            <div style={{ fontSize: 13.5, color: '#B7BEDD' }}>Upload an image and add context — most documents come back in under 15 seconds.</div>
          </div>
          <button className="btn btn-block" style={{ background: 'var(--marigold)', color: 'var(--indigo-deep)', flexShrink: 0 }} onClick={() => go('upload')}>
            <Plus size={16} /> Start transcription
          </button>
        </div>
      </div>

      <div className="card" style={{ padding: '10px 6px' }}>
        <div className="row between" style={{ padding: '10px 16px 4px' }}>
          <span style={{ fontWeight: 600, fontSize: 15 }}>Recent transcriptions</span>
          <a style={{ fontSize: 13.5, color: 'var(--indigo)', fontWeight: 600, cursor: 'pointer' }} onClick={() => go('history')}>View all</a>
        </div>
        {recent.map((d) => (
          <div className="doc-row" key={d.id} onClick={() => go('review')} style={{ cursor: 'pointer' }}>
            <span className="doc-thumb"><FileText size={17} /></span>
            <div>
              <div className="doc-title">{d.title}</div>
              <div className="doc-meta">{d.category} · {d.date}</div>
            </div>
            <span className="badge badge-indigo">{d.category}</span>
            <span className={`badge ${d.confidence >= 90 ? 'badge-sage' : 'badge-marigold'}`}>{d.confidence}% confidence</span>
            <ChevronRight size={16} color="var(--ink-faint)" />
          </div>
        ))}
      </div>
    </AppShell>
  );
}
