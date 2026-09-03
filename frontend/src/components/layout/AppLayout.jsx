import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(() => {
    return localStorage.getItem('pulseops_sidebar_collapsed') === 'true';
  });

  useEffect(() => {
    localStorage.setItem('pulseops_sidebar_collapsed', isCollapsed);
  }, [isCollapsed]);

  const toggleSidebar = () => setIsCollapsed(!isCollapsed);

  return (
    <div className={`app-layout ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
      <Sidebar
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
        isCollapsed={isCollapsed}
        onToggleSidebar={toggleSidebar}
      />
      <div className="app-container">
        <Header onToggleMobile={() => setMobileOpen(!mobileOpen)} />
        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
