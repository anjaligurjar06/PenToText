import { useEffect, useState } from 'react';
import { Check, Pencil, FileDown, Download, Copy } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { PageMock } from '../components/Shared.jsx';
import { CATEGORIES } from '../data.js';
import { api } from '../api.js';

export default function Review({ go, docId }) {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [plainText, setPlainText] = useState('');
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState('');

  useEffect(() => {
    if (!docId) {
      setError('No document selected.');
      setLoading(false);
      return;
    }
    api.getDocument(docId)
      .then((d) => {
        setDoc(d);
        setPlainText(d.transcript_text || '');
      })
      .catch((err) => setError(err.message || 'Could not load document'))
      .finally(() => setLoading(false));
  }, [docId]);

  function fireToast(msg) {
    setToast(msg);
    setTimeout(() => setToast(''), 2200);
  }

  async function handleSave() {
    if (!doc) return;
    setSaving(true);
    try {
      const updated = await api.updateDocument(doc.id, { transcript_text: plainText });
      setDoc(updated);
      setEditing(false);
      fireToast('Saved to your history');
    } catch (err) {
      fireToast(err.message || 'Could not save');
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <AppShell view="review" go={go}>
        <div className="page-sub">Loading…</div>
      </AppShell>
    );
  }

  if (error || !doc) {
    return (
      <AppShell view="review" go={go}>
        <div className="card" style={{ padding: 24 }}>
          <div style={{ color: 'var(--brick)', marginBottom: 12 }}>{error || 'Document not found.'}</div>
          <button className="btn btn-secondary" onClick={() => go('history')}>Back to history</button>
        </div>
      </AppShell>
    );
  }

  const catLabel = CATEGORIES.find((c) => c.id === doc.category)?.label || doc.category;

  return (
    <AppShell view="review" go={go}>
      <div className="topbar row between" style={{ alignItems: 'flex-start' }}>
        <div>
          <div className="page-title serif">{doc.title}</div>
          <div className="page-sub">{catLabel}{doc.context ? ` · ${doc.context}` : ''} · uploaded {new Date(doc.created_at).toLocaleDateString()}</div>
        </div>
        <span className={`badge ${doc.confidence != null && doc.confidence < 90 ? 'badge-marigold' : 'badge-sage'}`}>
          <Check size={13} /> {doc.confidence != null ? `${doc.confidence}% confidence` : doc.status}
        </span>
      </div>

      <div className="review-grid">
        <div className="card page-mock">
          <PageMock variant={doc.category} />
        </div>

        <div className="col" style={{ gap: 16 }}>
          <div className="card">
            <div className="row between" style={{ padding: '16px 20px 0' }}>
              <span style={{ fontWeight: 600, fontSize: 14.5 }}>Transcribed text</span>
              <button className="btn btn-ghost btn-sm" onClick={() => setEditing(!editing)}>
                <Pencil size={14} /> {editing ? 'Done editing' : 'Edit manually'}
              </button>
            </div>
            {editing ? (
              <div style={{ padding: 20 }}>
                <textarea
                  className="textarea mono"
                  style={{ minHeight: 200 }}
                  value={plainText}
                  onChange={(e) => setPlainText(e.target.value)}
                />
              </div>
            ) : (
              <div className="transcript-box mono">{plainText}</div>
            )}
          </div>

          <div className="action-bar">
            <button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? 'Saving…' : 'Save'}</button>
            <button className="btn btn-secondary" onClick={() => fireToast('Exported as PDF')}><FileDown size={15} /> Export PDF</button>
            <button className="btn btn-secondary" onClick={() => fireToast('Exported as DOCX')}><Download size={15} /> Export DOCX</button>
            <button className="btn btn-ghost" onClick={() => { navigator.clipboard?.writeText(plainText); fireToast('Copied to clipboard'); }}><Copy size={15} /> Copy text</button>
          </div>
        </div>
      </div>

      {toast && <div className="toast"><Check size={15} /> {toast}</div>}
    </AppShell>
  );
}
