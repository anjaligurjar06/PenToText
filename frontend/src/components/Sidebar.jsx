import { LayoutDashboard, Upload, History, LogOut } from 'lucide-react';

export default function Sidebar({ view, go }) {
  const items = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'upload', label: 'New upload', icon: Upload },
    { id: 'history', label: 'History', icon: History },
  ];
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
          <span className="sidebar-avatar">JE</span>
          <div>
            <div style={{ fontSize: 13.5, fontWeight: 600, color: '#fff' }}>Jordan Ellis</div>
            <div style={{ fontSize: 11.5, color: '#8B93BC' }}>jordan@example.com</div>
          </div>
        </div>
        <div className="snav">
          <button onClick={() => go('landing')}><LogOut size={16} /> Log out</button>
        </div>
      </div>
    </div>
  );
}
