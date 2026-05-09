import React from 'react';
import { getLang } from '../utils/languages.js';
import { clearHistory, removeFromHistory } from '../utils/history.js';

export function HistoryPanel({ history, setHistory, onRestore }) {
  if (history.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--text3)' }}>
        <div style={{ fontSize: 36, marginBottom: 12 }}>📋</div>
        <div style={{ fontSize: 15, fontWeight: 500 }}>No translation history yet</div>
        <div style={{ fontSize: 13, marginTop: 6 }}>Your translations will appear here</div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
        <span style={{ fontSize: 13, color: 'var(--text2)', fontWeight: 500 }}>{history.length} translation{history.length !== 1 ? 's' : ''}</span>
        <button
          onClick={() => { clearHistory(); setHistory([]); }}
          style={{
            fontSize: 12, color: 'var(--danger)', fontWeight: 500, padding: '4px 10px',
            border: '1px solid rgba(224,58,58,0.25)', borderRadius: 8,
            background: 'rgba(224,58,58,0.07)', cursor: 'pointer', transition: 'all 0.15s',
          }}
        >Clear All</button>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {history.map((item, i) => {
          const src = getLang(item.detectedLang || item.sourceLang);
          const tgt = getLang(item.targetLang);
          return (
            <div
              key={item.id}
              style={{
                padding: '14px 16px',
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: 14,
                cursor: 'pointer',
                transition: 'all 0.2s',
                animation: `fadeUp 0.3s ${i * 0.04}s both`,
              }}
              onClick={() => onRestore(item)}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 0 2px var(--accent-glow)'; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none'; }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <span style={{ fontSize: 13 }}>{src.flag} {src.name}</span>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M8 4l3 3-3 3" stroke="var(--text3)" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/></svg>
                <span style={{ fontSize: 13 }}>{tgt.flag} {tgt.name}</span>
                <button
                  onClick={e => {
                    e.stopPropagation();
                    const updated = removeFromHistory(item.id);
                    setHistory(updated);
                  }}
                  style={{ marginLeft: 'auto', color: 'var(--text3)', padding: 2, borderRadius: 6, background: 'none', border: 'none', cursor: 'pointer', lineHeight: 0 }}
                >
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M11 3L3 11M3 3l8 8" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>
                </button>
              </div>
              <div style={{ fontSize: 13, color: 'var(--text)', fontWeight: 500, marginBottom: 4, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {item.sourceText}
              </div>
              <div style={{ fontSize: 13, color: 'var(--text2)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {item.translatedText}
              </div>
              <div style={{ fontSize: 11, color: 'var(--text3)', marginTop: 8 }}>
                {new Date(item.timestamp).toLocaleString()}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
