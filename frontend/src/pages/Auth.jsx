import { useState } from 'react';
import { User, Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react';
import { Field } from '../components/Shared.jsx';
import { api, setSession } from '../api.js';

export default function Auth({ go, initialMode }) {
  const [mode, setMode] = useState(initialMode || 'login');
  const [showPw, setShowPw] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const result = mode === 'login'
        ? await api.login(email, password)
        : await api.register(name, email, password);
      setSession(result.access_token, result.user);
      go('dashboard');
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-brand">
        <a className="logo" onClick={() => go('landing')} style={{ cursor: 'pointer', color: '#fff' }}>
          <span className="logo-mark" style={{ background: 'var(--marigold)', color: 'var(--indigo-deep)' }}>P</span> PenToText
        </a>
        <div>
          <p className="auth-quote">
            "The context you give it is what turns a guess into a reading."
          </p>
          <p style={{ marginTop: 18, color: '#AEB6D8', fontSize: 14 }}>— from the design notes</p>
        </div>
        <div style={{ fontSize: 12.5, color: '#8B93BC' }}>© 2026 PenToText — portfolio project</div>
      </div>

      <div className="auth-form-wrap">
        <div style={{ width: '100%', maxWidth: 380 }}>
          <div className="auth-tabs">
            <button className={`auth-tab ${mode === 'login' ? 'active' : ''}`} onClick={() => setMode('login')}>Log in</button>
            <button className={`auth-tab ${mode === 'signup' ? 'active' : ''}`} onClick={() => setMode('signup')}>Create account</button>
          </div>

          <h2 className="serif" style={{ fontSize: 24, marginBottom: 6 }}>
            {mode === 'login' ? 'Welcome back' : 'Start transcribing'}
          </h2>
          <p style={{ color: 'var(--ink-soft)', fontSize: 14, marginBottom: 26 }}>
            {mode === 'login' ? 'Log in to reach your dashboard and history.' : 'Create an account to start transcribing.'}
          </p>

          <form className="col" style={{ gap: 16 }} onSubmit={handleSubmit}>
            {mode === 'signup' && (
              <Field label="Full name">
                <div className="input-icon-wrap">
                  <User size={16} />
                  <input className="input" placeholder="Jordan Ellis" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
              </Field>
            )}
            <Field label="Email">
              <div className="input-icon-wrap">
                <Mail size={16} />
                <input className="input" type="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
              </div>
            </Field>
            <Field label="Password">
              <div className="input-icon-wrap">
                <Lock size={16} />
                <input className="input" type={showPw ? 'text' : 'password'} placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required />
                <button type="button" className="eye-btn" onClick={() => setShowPw(!showPw)}>
                  {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </Field>
            {error && <div style={{ color: 'var(--brick)', fontSize: 13.5 }}>{error}</div>}
            <button className="btn btn-primary btn-block" type="submit" disabled={submitting} style={{ marginTop: 6 }}>
              {submitting ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'} <ArrowRight size={16} />
            </button>
          </form>

          <p style={{ textAlign: 'center', fontSize: 13.5, color: 'var(--ink-faint)', marginTop: 22 }}>
            {mode === 'login' ? "Don't have an account? " : 'Already have one? '}
            <a style={{ color: 'var(--indigo)', fontWeight: 600, cursor: 'pointer' }}
               onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}>
              {mode === 'login' ? 'Create one' : 'Log in'}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
