import { useState } from 'react';
import { AlertTriangle, Check, Pencil, FileDown, Download, Copy } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { PageMock, Field } from '../components/Shared.jsx';
import { TRANSCRIPT_TOKENS } from '../data.js';

export default function Review({ go }) {
  const [tokens, setTokens] = useState(
    TRANSCRIPT_TOKENS.map((t, i) => Array.isArray(t)
      ? { id: i, text: t[0], low: true, confirmed: false }
      : { id: i, text: t, low: false, confirmed: false })
  );
  const [editing, setEditing] = useState(false);
  const [plainText, setPlainText] = useState(TRANSCRIPT_TOKENS.map((t) => Array.isArray(t) ? t[0] : t).join(' '));
  const [toast, setToast] = useState('');

  function confirmWord(id) {
    setTokens((prev) => prev.map((t) => (t.id === id ? { ...t, confirmed: true } : t)));
  }

  function fireToast(msg) {
    setToast(msg);
    setTimeout(() => setToast(''), 2200);
  }

  const flaggedLeft = tokens.filter((t) => t.low && !t.confirmed).length;

  return (
    <AppShell view="review" go={go}>
      <div className="topbar row between" style={{ alignItems: 'flex-start' }}>
        <div>
          <div className="page-title serif">Follow-up prescription</div>
          <div className="page-sub">Prescription · dermatology · uploaded Jul 8, 2026</div>
        </div>
        <span className={`badge ${flaggedLeft ? 'badge-marigold' : 'badge-sage'}`}>
          {flaggedLeft ? <AlertTriangle size={13} /> : <Check size={13} />}
          {flaggedLeft ? `${flaggedLeft} word${flaggedLeft > 1 ? 's' : ''} to review` : 'All confirmed'}
        </span>
      </div>

      <div className="review-grid">
        <div className="card page-mock">
          <PageMock variant="prescription" />
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
              <div className="transcript-box mono">
                {tokens.map((t) => (
                  <span
                    key={t.id}
                    className={`word ${t.low && !t.confirmed ? 'low' : ''} ${t.confirmed ? 'confirmed' : ''}`}
                    onClick={() => t.low && !t.confirmed && confirmWord(t.id)}
                    title={t.low && !t.confirmed ? 'Low confidence — click to confirm' : undefined}
                  >
                    {t.text}
                  </span>
                ))}{' '}
              </div>
            )}
            <div className="row" style={{ gap: 16, padding: '4px 20px 18px', fontSize: 12.5, color: 'var(--ink-faint)' }}>
              <span className="row" style={{ gap: 6 }}><span className="legend-dot" style={{ background: 'var(--marigold-line)' }} /> Needs review</span>
              <span className="row" style={{ gap: 6 }}><span className="legend-dot" style={{ background: 'var(--sage)' }} /> Confirmed</span>
            </div>
          </div>

          <div className="card" style={{ padding: 20 }}>
            <div style={{ fontWeight: 600, fontSize: 14.5, marginBottom: 14 }}>Extracted fields</div>
            <div className="field-grid">
              <Field label="Medicine"><input className="input" defaultValue="Amoxicillin" /></Field>
              <Field label="Dosage"><input className="input" defaultValue="500 mg" /></Field>
              <Field label="Frequency"><input className="input" defaultValue="3× daily" /></Field>
              <Field label="Duration"><input className="input" defaultValue="7 days" /></Field>
            </div>
          </div>

          <div className="action-bar">
            <button className="btn btn-primary" onClick={() => fireToast('Saved to your history')}>Save</button>
            <button className="btn btn-secondary" onClick={() => fireToast('Exported as PDF')}><FileDown size={15} /> Export PDF</button>
            <button className="btn btn-secondary" onClick={() => fireToast('Exported as DOCX')}><Download size={15} /> Export DOCX</button>
            <button className="btn btn-ghost" onClick={() => fireToast('Copied to clipboard')}><Copy size={15} /> Copy text</button>
          </div>
        </div>
      </div>

      {toast && <div className="toast"><Check size={15} /> {toast}</div>}
    </AppShell>
  );
}
