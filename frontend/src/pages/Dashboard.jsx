import { useEffect, useState } from 'react';
import { Plus, FileText, ChevronRight } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { CATEGORIES } from '../data.js';
import { api, getSessionUser } from '../api.js';

function catLabel(catId) {
  return CATEGORIES.find((c) => c.id === catId)?.label || catId;
}

export default function Dashboard({ go }) {
  const [docs, setDocs] = useState([]);
  const user = getSessionUser();

  useEffect(() => {
    api.listDocuments().then(setDocs).catch(() => {});
  }, []);

  const recent = docs.slice(0, 4);
  const avgConfidence = docs.length
    ? Math.round(docs.reduce((sum, d) => sum + (d.confidence || 0), 0) / docs.length)
    : 0;
  const thisMonth = docs.filter((d) => {
    const created = new Date(d.created_at);
    const now = new Date();
    return created.getMonth() === now.getMonth() && created.getFullYear() === now.getFullYear();
  }).length;

  return (
    <AppShell view="dashboard" go={go}>
      <div className="topbar">
        <div className="page-title serif">Good afternoon{user?.name ? `, ${user.name.split(' ')[0]}` : ''}</div>
        <div className="page-sub">Here's what's happened since your last visit.</div>
      </div>

      <div className="stat-grid">
        <div className="card stat-card">
          <span className="lbl">Documents</span>
          <b>{docs.length}</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>transcribed total</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">This month</span>
          <b>{thisMonth}</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>documents</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">Avg. confidence</span>
          <b>{docs.length ? `${avgConfidence}%` : '—'}</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>across all documents</span>
        </div>
        <div className="card stat-card">
          <span className="lbl">Needs review</span>
          <b>{docs.filter((d) => (d.confidence ?? 100) < 90).length}</b>
          <span style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>documents flagged</span>
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
        {recent.length === 0 && (
          <div style={{ padding: '30px 20px', textAlign: 'center', color: 'var(--ink-faint)', fontSize: 14 }}>
            No documents yet — upload your first one to get started.
          </div>
        )}
        {recent.map((d) => (
          <div className="doc-row" key={d.id} onClick={() => go('review', d.id)} style={{ cursor: 'pointer' }}>
            <span className="doc-thumb"><FileText size={17} /></span>
            <div>
              <div className="doc-title">{d.title}</div>
              <div className="doc-meta">{catLabel(d.category)} · {new Date(d.created_at).toLocaleDateString()}</div>
            </div>
            <span className="badge badge-indigo">{catLabel(d.category)}</span>
            <span className={`badge ${(d.confidence ?? 0) >= 90 ? 'badge-sage' : 'badge-marigold'}`}>{d.confidence ?? '—'}% confidence</span>
            <ChevronRight size={16} color="var(--ink-faint)" />
          </div>
        ))}
      </div>
    </AppShell>
  );
}
