import React from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import { Activity, LayoutDashboard, Radio, AlertTriangle, Bell, Settings, LogOut, X, ChevronLeft, ChevronRight } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Sidebar({ mobileOpen, onCloseMobile, isCollapsed, onToggleSidebar }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (onCloseMobile) onCloseMobile();
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <>
      {mobileOpen && (
        <div className="mobile-overlay" onClick={onCloseMobile} />
      )}
      <aside className={`app-sidebar ${mobileOpen ? 'mobile-open' : ''}`}>
        <div className="sidebar-header" style={{ padding: isCollapsed ? '0' : '0 var(--space-5)', justifyContent: isCollapsed ? 'center' : 'space-between' }}>
          {!isCollapsed ? (
            <Link to="/" className="public-brand" onClick={onCloseMobile}>
              <Activity size={20} className="public-brand-icon" />
              <span>PulseOps</span>
            </Link>
          ) : (
            <Link to="/" className="public-brand" onClick={onCloseMobile}>
              <Activity size={20} className="public-brand-icon" />
            </Link>
          )}

          {mobileOpen ? (
            <button className="menu-toggle-btn desktop-hide" onClick={onCloseMobile} aria-label="Close Navigation">
              <X size={18} />
            </button>
          ) : (
            <button 
              className="menu-toggle-btn mobile-hide desktop-collapse-btn" 
              onClick={onToggleSidebar} 
              aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
              title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
              style={{ display: 'flex' }}
            >
              {isCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
          )}
        </div>

        <nav className="sidebar-nav">
          <NavLink
            to="/dashboard"
            onClick={onCloseMobile}
            className={({ isActive }) => (isActive ? 'sidebar-link active' : 'sidebar-link')}
            title={isCollapsed ? "Dashboard" : undefined}
          >
            <LayoutDashboard size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Dashboard</span>}
          </NavLink>

          <NavLink
            to="/monitors"
            onClick={onCloseMobile}
            className={({ isActive }) => (isActive ? 'sidebar-link active' : 'sidebar-link')}
            title={isCollapsed ? "Monitors" : undefined}
          >
            <Radio size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Monitors</span>}
          </NavLink>

          <NavLink
            to="/incidents"
            onClick={onCloseMobile}
            className={({ isActive }) => (isActive ? 'sidebar-link active' : 'sidebar-link')}
            title={isCollapsed ? "Incidents" : undefined}
          >
            <AlertTriangle size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Incidents</span>}
          </NavLink>

          <NavLink
            to="/notifications"
            onClick={onCloseMobile}
            className={({ isActive }) => (isActive ? 'sidebar-link active' : 'sidebar-link')}
            title={isCollapsed ? "Notifications" : undefined}
          >
            <Bell size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Notifications</span>}
          </NavLink>

          <NavLink
            to="/settings"
            onClick={onCloseMobile}
            className={({ isActive }) => (isActive ? 'sidebar-link active' : 'sidebar-link')}
            title={isCollapsed ? "Settings" : undefined}
          >
            <Settings size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Settings</span>}
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <button
            type="button"
            className="sidebar-link"
            onClick={handleLogout}
            title={isCollapsed ? "Logout" : undefined}
            style={{ width: '100%', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left', justifyContent: isCollapsed ? 'center' : 'flex-start' }}
          >
            <LogOut size={18} style={{ flexShrink: 0 }} />
            {!isCollapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>
    </>
  );
}
