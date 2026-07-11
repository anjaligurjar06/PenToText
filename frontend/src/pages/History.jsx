import { useState } from 'react';
import { Search, FileText, Clock, Eye, Trash2 } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { CATEGORIES, HISTORY_DOCS } from '../data.js';

export default function History({ go }) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');

  const filtered = HISTORY_DOCS.filter((d) => {
    const matchesQuery = d.title.toLowerCase().includes(query.toLowerCase());
    const matchesFilter = filter === 'all' || d.catId === filter;
    return matchesQuery && matchesFilter;
  });

  return (
    <AppShell view="history" go={go}>
      <div className="topbar">
        <div className="page-title serif">History</div>
        <div className="page-sub">{HISTORY_DOCS.length} documents transcribed so far.</div>
      </div>

      <div className="filter-row">
        <div className="input-icon-wrap" style={{ width: 260 }}>
          <Search size={16} />
          <input className="input" placeholder="Search documents…" value={query} onChange={(e) => setQuery(e.target.value)} />
        </div>
        <button className={`chip ${filter === 'all' ? 'selected' : ''}`} onClick={() => setFilter('all')}>All</button>
        {CATEGORIES.map((c) => (
          <button key={c.id} className={`chip ${filter === c.id ? 'selected' : ''}`} onClick={() => setFilter(c.id)}>
            <c.icon size={14} /> {c.label}
          </button>
        ))}
      </div>

      <div className="card table-wrap" style={{ padding: '10px 6px' }}>
        <div className="table-head">
          <span></span><span>Document</span><span>Category</span><span>Date</span><span>Confidence</span><span></span>
        </div>
        {filtered.length === 0 && (
          <div style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--ink-faint)', fontSize: 14 }}>
            Nothing matches that search yet.
          </div>
        )}
        {filtered.map((d) => (
          <div className="doc-row" key={d.id}>
            <span className="doc-thumb"><FileText size={17} /></span>
            <div className="doc-title" style={{ cursor: 'pointer' }} onClick={() => go('review')}>{d.title}</div>
            <span style={{ fontSize: 13.5, color: 'var(--ink-soft)' }}>{d.category}</span>
            <span className="row" style={{ gap: 6, fontSize: 13.5, color: 'var(--ink-soft)' }}><Clock size={13} /> {d.date}</span>
            <span className={`badge ${d.confidence >= 90 ? 'badge-sage' : 'badge-marigold'}`}>{d.confidence}%</span>
            <div className="row" style={{ gap: 4 }}>
              <button className="btn btn-ghost btn-sm" onClick={() => go('review')} title="View"><Eye size={15} /></button>
              <button className="btn btn-ghost btn-sm" title="Delete"><Trash2 size={15} color="var(--brick)" /></button>
            </div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
