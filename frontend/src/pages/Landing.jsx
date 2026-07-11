import { ArrowRight, Check, AlertTriangle, ShieldCheck } from 'lucide-react';
import MarketingNav from '../components/MarketingNav.jsx';
import Footer from '../components/Footer.jsx';
import { HeroDemo } from '../components/Shared.jsx';
import { CATEGORIES } from '../data.js';

export default function Landing({ go }) {
  return (
    <div>
      <MarketingNav go={go} />

      <section className="hero">
        <div className="wrap hero-grid">
          <div>
            <span className="eyebrow">Context-aware transcription</span>
            <h1 className="serif">
              Handwriting is hard to read.<br />Tell it <em>why</em>, and it isn't.
            </h1>
            <p className="lead">
              PenToText turns prescriptions, exam scripts, and lecture notes into clean, editable
              text — using the context you provide about the document to resolve the words a
              generic scanner would guess wrong.
            </p>
            <div className="row" style={{ gap: 12 }}>
              <button className="btn btn-primary" onClick={() => go('auth', 'signup')}>
                Get started <ArrowRight size={16} />
              </button>
              <button className="btn btn-secondary" onClick={() => go('dashboard')}>
                See a live demo
              </button>
            </div>
            <div className="hero-stats">
              <div className="hero-stat"><b>15s</b><span>Typical turnaround</span></div>
              <div className="hero-stat"><b>4</b><span>Document categories</span></div>
              <div className="hero-stat"><b>PDF / DOCX</b><span>Export formats</span></div>
            </div>
          </div>
          <HeroDemo />
        </div>
      </section>

      <section className="section" id="how">
        <div className="wrap">
          <div className="section-head">
            <span className="eyebrow">Three steps, start to finish</span>
            <h2 className="serif">Upload-to-result in under a minute</h2>
            <p>No configuration, no training your own model. Tell PenToText what the document is, and let it do the reading.</p>
          </div>
          <div className="steps">
            <div className="step">
              <span className="step-num mono">01</span>
              <h3>Upload the image</h3>
              <p>A photo or scan of the handwritten page — a prescription pad, an answer script, a page of notes.</p>
            </div>
            <div className="step">
              <span className="step-num mono">02</span>
              <h3>Add context</h3>
              <p>Pick a category and add a hint — the diagnosed condition, the exam subject, the course topic.</p>
            </div>
            <div className="step">
              <span className="step-num mono">03</span>
              <h3>Review &amp; export</h3>
              <p>Read the typed result beside the original, fix anything flagged, then export or save it.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="categories" style={{ background: 'var(--paper-deep)' }}>
        <div className="wrap">
          <div className="section-head">
            <span className="eyebrow">Built for specific handwriting</span>
            <h2 className="serif">Four document types, one engine</h2>
            <p>Each category prompts for the context that actually moves the needle on accuracy.</p>
          </div>
          <div className="cat-grid">
            {CATEGORIES.map((c) => (
              <div className="card cat-card" key={c.id}>
                <span className="cat-icon"><c.icon size={20} /></span>
                <h4>{c.label}</h4>
                <p>{c.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section" id="trust">
        <div className="wrap" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 56, alignItems: 'center' }}>
          <div>
            <span className="eyebrow">Low-confidence flagging</span>
            <h2 className="serif" style={{ marginTop: 14 }}>You always see what it wasn't sure about</h2>
            <p style={{ color: 'var(--ink-soft)', fontSize: 16, lineHeight: 1.6, marginBottom: 20 }}>
              Rather than silently guessing, PenToText marks the words it's uncertain of — like a
              drug name it can't fully match — so review takes seconds, not a full re-read.
            </p>
            <div className="row" style={{ gap: 14 }}>
              <span className="badge badge-marigold"><AlertTriangle size={13} /> Needs review</span>
              <span className="badge badge-sage"><Check size={13} /> Confirmed</span>
            </div>
          </div>
          <div className="card" style={{ padding: 24 }}>
            <div className="row" style={{ gap: 8, marginBottom: 14 }}>
              <ShieldCheck size={17} color="var(--indigo)" />
              <span style={{ fontWeight: 600, fontSize: 14.5 }}>Private by default</span>
            </div>
            <p style={{ fontSize: 13.8, color: 'var(--ink-soft)', lineHeight: 1.65 }}>
              Uploaded documents — including medical content — are encrypted in transit and
              visible only to the account that uploaded them. Delete any document, and its data
              is removed permanently.
            </p>
          </div>
        </div>
      </section>

      <Footer go={go} />
    </div>
  );
}
