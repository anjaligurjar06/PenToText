import { LayoutDashboard, Upload, History, LogOut } from 'lucide-react';
import { clearSession, getSessionUser } from '../api.js';

export default function Sidebar({ view, go }) {
  const items = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'upload', label: 'New upload', icon: Upload },
    { id: 'history', label: 'History', icon: History },
  ];
  const user = getSessionUser();
  const initials = user?.name
    ? user.name.split(' ').map((p) => p[0]).slice(0, 2).join('').toUpperCase()
    : '?';

  function handleLogout() {
    clearSession();
    go('landing');
  }

  return (
    <div className="sidebar">
      <a className="logo" onClick={() => go('landing')} style={{ cursor: 'pointer' }}>
        <span className="logo-mark">P</span> PenToText
      </a>
      <div className="snav">
        {items.map((it) => (
          <button key={it.id} className={view === it.id ? 'active' : ''} onClick={() => go(it.id)}>
            <it.icon size={17} /> {it.label}
          </button>
        ))}
      </div>
      <div className="sidebar-bottom">
        <div className="sidebar-user">
          <span className="sidebar-avatar">{initials}</span>
          <div>
            <div style={{ fontSize: 13.5, fontWeight: 600, color: '#fff' }}>{user?.name || 'Guest'}</div>
            <div style={{ fontSize: 11.5, color: '#8B93BC' }}>{user?.email || ''}</div>
          </div>
        </div>
        <div className="snav">
          <button onClick={handleLogout}><LogOut size={16} /> Log out</button>
        </div>
      </div>
    </div>
  );
}
