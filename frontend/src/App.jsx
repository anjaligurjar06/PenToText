import { useState } from 'react';
import Landing from './pages/Landing.jsx';
import Auth from './pages/Auth.jsx';
import Dashboard from './pages/Dashboard.jsx';
import UploadPage from './pages/Upload.jsx';
import Review from './pages/Review.jsx';
import History from './pages/History.jsx';

export default function App() {
  const [view, setView] = useState('landing');
  const [authMode, setAuthMode] = useState('login');
  const [activeDocId, setActiveDocId] = useState(null);

  function go(next, arg) {
    if (next === 'auth' && arg) setAuthMode(arg);
    if (next === 'review') setActiveDocId(arg ?? null);
    setView(next);
    window.scrollTo?.(0, 0);
  }

  return (
    <div className="ptt">
      {view === 'landing' && <Landing go={go} />}
      {view === 'auth' && <Auth go={go} initialMode={authMode} />}
      {view === 'dashboard' && <Dashboard go={go} />}
      {view === 'upload' && <UploadPage go={go} />}
      {view === 'review' && <Review go={go} docId={activeDocId} />}
      {view === 'history' && <History go={go} />}
    </div>
  );
}
