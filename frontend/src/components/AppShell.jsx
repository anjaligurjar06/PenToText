import Sidebar from './Sidebar.jsx';

export default function AppShell({ view, go, children }) {
  return (
    <div className="shell">
      <Sidebar view={view} go={go} />
      <div className="main">{children}</div>
    </div>
  );
}
