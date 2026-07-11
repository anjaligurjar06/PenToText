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

  function go(next, mode) {
    if (next === 'auth' && mode) setAuthMode(mode);
    setView(next);
    window.scrollTo?.(0, 0);
  }

  return (
    <div className="ptt">
      {view === 'landing' && <Landing go={go} />}
      {view === 'auth' && <Auth go={go} initialMode={authMode} />}
      {view === 'dashboard' && <Dashboard go={go} />}
      {view === 'upload' && <UploadPage go={go} />}
      {view === 'review' && <Review go={go} />}
      {view === 'history' && <History go={go} />}
    </div>
  );
}
