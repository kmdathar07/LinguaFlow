import React from 'react';

const ICONS = {
  success: (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M5 8l2 2 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  error: (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M10 6L6 10M6 6l4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  ),
  info: (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M8 7.5v4M8 5.5v.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  ),
};

const COLORS = {
  success: { bg: 'rgba(20,184,112,0.12)', border: 'rgba(20,184,112,0.3)', color: '#14b870' },
  error: { bg: 'rgba(224,58,58,0.12)', border: 'rgba(224,58,58,0.3)', color: '#e03a3a' },
  info: { bg: 'rgba(79,47,219,0.1)', border: 'rgba(79,47,219,0.25)', color: 'var(--accent2)' },
};

export function ToastContainer({ toasts, dismiss }) {
  return (
    <div style={{
      position: 'fixed', top: 24, right: 24, zIndex: 9999,
      display: 'flex', flexDirection: 'column', gap: 10,
      pointerEvents: 'none',
    }}>
      {toasts.map(t => {
        const c = COLORS[t.type] || COLORS.info;
        return (
          <div
            key={t.id}
            onClick={() => dismiss(t.id)}
            style={{
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '12px 16px',
              background: `var(--surface)`,
              backdropFilter: 'blur(20px)',
              border: `1px solid ${c.border}`,
              borderRadius: 14,
              boxShadow: 'var(--shadow-lg)',
              color: c.color,
              fontSize: 14,
              fontFamily: 'var(--font-body)',
              fontWeight: 500,
              pointerEvents: 'auto',
              cursor: 'pointer',
              maxWidth: 320,
              animation: t.exiting
                ? 'toastOut 0.3s cubic-bezier(0.4,0,0.2,1) forwards'
                : 'toastIn 0.35s cubic-bezier(0.34,1.56,0.64,1) forwards',
            }}
          >
            <span style={{ flexShrink: 0 }}>{ICONS[t.type]}</span>
            <span style={{ color: 'var(--text)', fontWeight: 450 }}>{t.message}</span>
          </div>
        );
      })}
    </div>
  );
}
