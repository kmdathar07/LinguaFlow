import React, { useState, useRef, useEffect } from 'react';
import { LANGUAGES, TARGET_LANGUAGES, getLang } from '../utils/languages.js';

export function LanguageSelector({ value, onChange, includeAuto = false, label }) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);
  const inputRef = useRef(null);
  const list = includeAuto ? LANGUAGES : TARGET_LANGUAGES;
  const filtered = list.filter(l =>
    l.name.toLowerCase().includes(search.toLowerCase()) ||
    l.code.toLowerCase().includes(search.toLowerCase())
  );
  const selected = getLang(value);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  useEffect(() => {
    if (open && inputRef.current) { inputRef.current.focus(); setSearch(''); }
  }, [open]);

  return (
    <div ref={ref} style={{ position: 'relative', minWidth: 0, flex: 1 }}>
      {label && (
        <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 8, fontFamily: 'var(--font-display)' }}>
          {label}
        </div>
      )}
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%',
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '11px 14px',
          background: 'var(--surface)',
          border: `1.5px solid ${open ? 'var(--accent)' : 'var(--border)'}`,
          borderRadius: 'var(--radius-sm)',
          color: 'var(--text)',
          fontSize: 14, fontWeight: 500,
          cursor: 'pointer',
          transition: 'all 0.2s',
          backdropFilter: 'blur(12px)',
          boxShadow: open ? `0 0 0 3px var(--accent-glow)` : 'none',
        }}
      >
        <span style={{ fontSize: 18 }}>{selected.flag}</span>
        <span style={{ flex: 1, textAlign: 'left', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {selected.name}
        </span>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style={{ flexShrink: 0, transform: open ? 'rotate(180deg)' : '', transition: 'transform 0.2s' }}>
          <path d="M3 5l4 4 4-4" stroke="var(--text2)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {open && (
        <div style={{
          position: 'absolute', top: 'calc(100% + 8px)', left: 0, right: 0, zIndex: 100,
          background: 'var(--bg)',
          border: '1.5px solid var(--border)',
          borderRadius: 'var(--radius-sm)',
          boxShadow: 'var(--shadow-lg)',
          overflow: 'hidden',
          backdropFilter: 'blur(24px)',
          animation: 'slideDown 0.18s cubic-bezier(0.4,0,0.2,1)',
        }}>
          <div style={{ padding: '10px 10px 6px' }}>
            <input
              ref={inputRef}
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search language..."
              style={{
                width: '100%', padding: '8px 12px',
                background: 'var(--surface2)',
                border: '1px solid var(--border)',
                borderRadius: 8, fontSize: 13,
                color: 'var(--text)', outline: 'none',
              }}
            />
          </div>
          <div style={{ maxHeight: 240, overflowY: 'auto' }}>
            {filtered.length === 0 ? (
              <div style={{ padding: '16px', textAlign: 'center', color: 'var(--text3)', fontSize: 13 }}>No results</div>
            ) : filtered.map(lang => (
              <button
                key={lang.code}
                onClick={() => { onChange(lang.code); setOpen(false); }}
                style={{
                  width: '100%', display: 'flex', alignItems: 'center', gap: 10,
                  padding: '9px 14px',
                  background: lang.code === value ? 'var(--accent-glow)' : 'transparent',
                  border: 'none', cursor: 'pointer',
                  color: lang.code === value ? 'var(--accent2)' : 'var(--text)',
                  fontSize: 13, fontWeight: lang.code === value ? 600 : 400,
                  textAlign: 'left', transition: 'background 0.15s',
                }}
                onMouseEnter={e => { if (lang.code !== value) e.currentTarget.style.background = 'var(--surface)'; }}
                onMouseLeave={e => { if (lang.code !== value) e.currentTarget.style.background = 'transparent'; }}
              >
                <span style={{ fontSize: 16 }}>{lang.flag}</span>
                <span>{lang.name}</span>
                {lang.code === value && (
                  <svg style={{ marginLeft: 'auto' }} width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M3 7l3 3 5-5" stroke="var(--accent2)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
