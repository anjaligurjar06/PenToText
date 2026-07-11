import { useState } from 'react';
import { FileText, ImagePlus, Sparkles } from 'lucide-react';
import AppShell from '../components/AppShell.jsx';
import { Field } from '../components/Shared.jsx';
import { CATEGORIES } from '../data.js';

export default function UploadPage({ go }) {
  const [category, setCategory] = useState('prescription');
  const [fileName, setFileName] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState('Reading the image…');

  const cat = CATEGORIES.find((c) => c.id === category);

  function handleSubmit() {
    setSubmitting(true);
    const msgs = ['Reading the image…', 'Matching context…', 'Typing it up…'];
    let i = 0;
    setLoadingMsg(msgs[0]);
    const interval = setInterval(() => {
      i++;
      if (i < msgs.length) setLoadingMsg(msgs[i]);
    }, 500);
    setTimeout(() => {
      clearInterval(interval);
      setSubmitting(false);
      go('review');
    }, 1600);
  }

  return (
    <AppShell view="upload" go={go}>
      <div className="topbar">
        <div className="page-title serif">New transcription</div>
        <div className="page-sub">Upload an image, tell us what it is, and we'll do the reading.</div>
      </div>

      <div className="upload-steps">
        <div className="card" style={{ padding: 26 }}>
          <div className="u-step-label"><span className="u-step-num">1</span> Upload the document</div>
          <div
            className={`dropzone ${dragOver ? 'active' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setDragOver(false); setFileName(e.dataTransfer.files?.[0]?.name || 'scanned-document.jpg'); }}
          >
            {fileName ? (
              <div className="col center" style={{ gap: 10 }}>
                <span className="cat-icon" style={{ margin: '0 auto' }}><FileText size={20} /></span>
                <div style={{ fontWeight: 600, fontSize: 14.5 }}>{fileName}</div>
                <button className="btn btn-ghost btn-sm" onClick={() => setFileName('')}>Choose a different file</button>
              </div>
            ) : (
              <div className="col center" style={{ gap: 10 }}>
                <ImagePlus size={26} color="var(--ink-faint)" />
                <div style={{ fontWeight: 600, fontSize: 14.5 }}>Drag an image here, or</div>
                <label className="btn btn-secondary btn-sm" style={{ cursor: 'pointer' }}>
                  Browse files
                  <input type="file" accept="image/*" style={{ display: 'none' }} onChange={(e) => setFileName(e.target.files?.[0]?.name || 'scanned-document.jpg')} />
                </label>
                <div style={{ fontSize: 12.5, color: 'var(--ink-faint)' }}>JPG, PNG, or PDF up to 20MB</div>
              </div>
            )}
          </div>
        </div>

        <div className="card" style={{ padding: 26 }}>
          <div className="u-step-label"><span className="u-step-num">2</span> Choose a category</div>
          <div className="chip-row">
            {CATEGORIES.map((c) => (
              <button key={c.id} className={`chip ${category === c.id ? 'selected' : ''}`} onClick={() => setCategory(c.id)}>
                <c.icon size={16} /> {c.label}
              </button>
            ))}
          </div>
        </div>

        <div className="card" style={{ padding: 26 }}>
          <div className="u-step-label"><span className="u-step-num">3</span> Add context</div>
          <div className="col" style={{ gap: 16 }}>
            <Field label="Document title">
              <input className="input" placeholder="e.g. Follow-up prescription, July 2026" />
            </Field>
            <Field label={cat.hint}>
              <input className="input" placeholder={
                category === 'prescription' ? 'e.g. Streptococcal pharyngitis' :
                category === 'exam' ? 'e.g. Organic Chemistry' :
                category === 'notes' ? 'e.g. Cardiology rotation' : 'Anything that helps — optional'
              } />
            </Field>
            <Field label="Additional notes (optional)">
              <textarea className="textarea" placeholder="Anything else the transcription engine should know…" />
            </Field>
          </div>
        </div>

        <div className="row between">
          <button className="btn btn-ghost" onClick={() => go('dashboard')}>Cancel</button>
          <button className="btn btn-primary" disabled={!fileName} onClick={handleSubmit}>
            <Sparkles size={16} /> Transcribe document
          </button>
        </div>
      </div>

      {submitting && (
        <div className="loading-overlay">
          <div className="loading-card">
            <div className="spinner" />
            <div style={{ fontWeight: 600 }}>{loadingMsg}</div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
