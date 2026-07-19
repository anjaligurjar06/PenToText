import { useEffect, useState } from 'react';
import { Search, FileText, Clock, Eye, Trash2 } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { CATEGORIES } from '../data.js';
import { api } from '../api.js';

function catLabel(catId) {
  return CATEGORIES.find((c) => c.id === catId)?.label || catId;
}

export default function History({ go }) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.listDocuments()
      .then(setDocs)
      .catch((err) => setError(err.message || 'Could not load history'))
      .finally(() => setLoading(false));
  }, []);

  async function handleDelete(id) {
    try {
      await api.deleteDocument(id);
      setDocs((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      setError(err.message || 'Could not delete document');
    }
  }

  const filtered = docs.filter((d) => {
    const matchesQuery = d.title.toLowerCase().includes(query.toLowerCase());
    const matchesFilter = filter === 'all' || d.category === filter;
    return matchesQuery && matchesFilter;
  });

  return (
    <AppShell view="history" go={go}>
      <div className="topbar">
        <div className="page-title serif">History</div>
        <div className="page-sub">{loading ? 'Loading…' : `${docs.length} documents transcribed so far.`}</div>
      </div>
      {error && <div style={{ color: 'var(--brick)', fontSize: 13.5, marginBottom: 12 }}>{error}</div>}

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
        {!loading && filtered.length === 0 && (
          <div style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--ink-faint)', fontSize: 14 }}>
            Nothing matches that search yet.
          </div>
        )}
        {filtered.map((d) => (
          <div className="doc-row" key={d.id}>
            <span className="doc-thumb"><FileText size={17} /></span>
            <div className="doc-title" style={{ cursor: 'pointer' }} onClick={() => go('review', d.id)}>{d.title}</div>
            <span style={{ fontSize: 13.5, color: 'var(--ink-soft)' }}>{catLabel(d.category)}</span>
            <span className="row" style={{ gap: 6, fontSize: 13.5, color: 'var(--ink-soft)' }}><Clock size={13} /> {new Date(d.created_at).toLocaleDateString()}</span>
            <span className={`badge ${d.confidence >= 90 ? 'badge-sage' : 'badge-marigold'}`}>{d.confidence ?? '—'}%</span>
            <div className="row" style={{ gap: 4 }}>
              <button className="btn btn-ghost btn-sm" onClick={() => go('review', d.id)} title="View"><Eye size={15} /></button>
              <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(d.id)} title="Delete"><Trash2 size={15} color="var(--brick)" /></button>
            </div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
