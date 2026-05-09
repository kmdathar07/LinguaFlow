import React from 'react';

export function Header({ theme, toggleTheme }) {
  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '20px 32px',
      borderBottom: '1px solid var(--border)',
      background: 'var(--surface)',
      backdropFilter: 'blur(20px)',
      position: 'sticky', top: 0, zIndex: 50,
    }}>
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{
          width: 36, height: 36,
          background: 'linear-gradient(135deg, var(--accent) 0%, var(--cyan) 100%)',
          borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 4px 12px var(--accent-glow)',
        }}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M3 5h8M7 3v2M5 5c0 3.3 2.7 6 6 6" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M11 11c-1.5 0-2.8.7-3.7 1.8M10 10l7 7" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <div>
          <div style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: 18, letterSpacing: '-0.01em', lineHeight: 1 }}>
            LinguaFlow
          </div>
          <div style={{ fontSize: 11, color: 'var(--text3)', fontWeight: 400, letterSpacing: '0.04em' }}>
            AI TRANSLATOR
          </div>
        </div>
      </div>

      {/* Nav */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <a href="https://github.com" target="_blank" rel="noreferrer" style={{
          display: 'flex', alignItems: 'center', gap: 6,
          fontSize: 13, fontWeight: 500, color: 'var(--text2)',
          padding: '7px 14px', borderRadius: 10,
          border: '1px solid var(--border)',
          background: 'var(--surface2)',
          textDecoration: 'none', transition: 'all 0.2s',
        }}
          onMouseEnter={e => { e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.borderColor = 'var(--border-strong)'; }}
          onMouseLeave={e => { e.currentTarget.style.color = 'var(--text2)'; e.currentTarget.style.borderColor = 'var(--border)'; }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.37.6.11.82-.26.82-.58v-2.03c-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.1-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02 0 2.04.13 3 .4 2.28-1.55 3.29-1.23 3.29-1.23.64 1.66.24 2.88.12 3.18.77.84 1.23 1.91 1.23 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.21.7.82.58C20.56 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/>
          </svg>
          GitHub
        </a>

        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          style={{
            width: 38, height: 38,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            borderRadius: 10,
            border: '1px solid var(--border)',
            background: 'var(--surface2)',
            color: 'var(--text2)',
            transition: 'all 0.2s', cursor: 'pointer',
          }}
          onMouseEnter={e => { e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.borderColor = 'var(--border-strong)'; }}
          onMouseLeave={e => { e.currentTarget.style.color = 'var(--text2)'; e.currentTarget.style.borderColor = 'var(--border)'; }}
        >
          {theme === 'dark' ? (
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="3.5" stroke="currentColor" strokeWidth="1.4"/>
              <path d="M8 1.5V3M8 13v1.5M1.5 8H3M13 8h1.5M3.5 3.5l1 1M11.5 11.5l1 1M11.5 3.5l-1 1M3.5 11.5l-1 1" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M13.5 9A6 6 0 0 1 7 2.5a5.5 5.5 0 1 0 6.5 6.5z" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </button>
      </div>
    </header>
  );
}
