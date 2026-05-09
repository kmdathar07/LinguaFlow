import React, { useState } from 'react';
import { Header } from './components/Header.jsx';
import { TranslatorCard } from './components/TranslatorCard.jsx';
import { HistoryPanel } from './components/HistoryPanel.jsx';
import { ToastContainer } from './components/Toast.jsx';
import { BackgroundOrbs } from './components/BackgroundOrbs.jsx';
import { useTheme } from './hooks/useTheme.js';
import { useToast } from './hooks/useToast.js';
import { getHistory } from './utils/history.js';

export default function App() {
  const { theme, toggle } = useTheme();
  const { toasts, toast, dismiss } = useToast();
  const [history, setHistory] = useState(() => getHistory());
  const [activeTab, setActiveTab] = useState('translate');
  const [restoreData, setRestoreData] = useState(null);

  const handleRestore = (item) => {
    setRestoreData(item);
    setActiveTab('translate');
  };

  return (
    <div style={{ minHeight: '100vh', position: 'relative' }}>
      <BackgroundOrbs />
      <div style={{ position: 'relative', zIndex: 1 }}>
        <Header theme={theme} toggleTheme={toggle} />

        <main style={{ maxWidth: 1100, margin: '0 auto', padding: '32px 24px 80px' }}>

          {/* Hero */}
          <div style={{ textAlign: 'center', marginBottom: 40, animation: 'fadeUp 0.6s both' }}>
            <h1 style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(36px, 5vw, 58px)',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              lineHeight: 1.1,
              marginBottom: 14,
              background: 'linear-gradient(135deg, var(--text) 30%, var(--accent2) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}>
              Break Every Language Barrier
            </h1>
            <p style={{
              fontSize: 17, color: 'var(--text2)', fontWeight: 400, maxWidth: 520, margin: '0 auto',
              lineHeight: 1.6,
            }}>
              AI-powered translation across 30+ languages. Preserving tone, context, and meaning in every word.
            </p>
          </div>

          {/* Tab pills */}
          <div style={{ display: 'flex', gap: 6, marginBottom: 20, justifyContent: 'center' }}>
            {[
              { id: 'translate', label: 'Translate', icon: '⚡' },
              { id: 'history', label: `History (${history.length})`, icon: '🕐' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 7,
                  padding: '9px 20px', borderRadius: 24,
                  border: `1.5px solid ${activeTab === tab.id ? 'var(--accent)' : 'var(--border)'}`,
                  background: activeTab === tab.id ? 'var(--accent-glow)' : 'var(--surface2)',
                  color: activeTab === tab.id ? 'var(--accent2)' : 'var(--text2)',
                  fontFamily: 'var(--font-body)',
                  fontSize: 14, fontWeight: activeTab === tab.id ? 600 : 400,
                  cursor: 'pointer', transition: 'all 0.2s',
                  backdropFilter: 'blur(12px)',
                }}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Content */}
          <div style={{ animation: 'fadeUp 0.5s 0.1s both' }}>
            {activeTab === 'translate' ? (
              <TranslatorCard toast={toast} setHistory={setHistory} restoreData={restoreData} />
            ) : (
              <div style={{
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                boxShadow: 'var(--shadow-lg)',
                backdropFilter: 'blur(24px)',
                padding: '24px',
              }}>
                <HistoryPanel history={history} setHistory={setHistory} onRestore={handleRestore} />
              </div>
            )}
          </div>

          {/* Feature badges */}
          <div style={{
            display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center',
            marginTop: 40, animation: 'fadeUp 0.5s 0.3s both',
          }}>
            {[
              { icon: '🧠', text: 'Google Gemini AI' },
              { icon: '⚡', text: 'Real-time Translation' },
              { icon: '🌍', text: '30+ Languages' },
              { icon: '🎙️', text: 'Voice Input & Output' },
              { icon: '🔄', text: 'Auto Language Detection' },
              { icon: '📋', text: 'Translation History' },
            ].map(f => (
              <div key={f.text} style={{
                display: 'flex', alignItems: 'center', gap: 7,
                padding: '7px 14px', borderRadius: 20,
                border: '1px solid var(--border)',
                background: 'var(--surface2)',
                backdropFilter: 'blur(12px)',
                fontSize: 13, color: 'var(--text2)',
              }}>
                <span>{f.icon}</span>
                <span>{f.text}</span>
              </div>
            ))}
          </div>
        </main>

        {/* Footer */}
        <footer style={{
          textAlign: 'center', padding: '20px',
          borderTop: '1px solid var(--border)',
          fontSize: 13, color: 'var(--text3)',
        }}>
          Built with ❤️ using Claude AI · LinguaFlow v1.0
        </footer>
      </div>

      <ToastContainer toasts={toasts} dismiss={dismiss} />
    </div>
  );
}
