import React, { useState, useRef, useEffect, useCallback } from 'react';
import { LanguageSelector } from './LanguageSelector.jsx';
import { useDebounce } from '../hooks/useDebounce.js';
import { useSpeech } from '../hooks/useSpeech.js';
import { translateText } from '../utils/api.js';
import { addToHistory, getHistory } from '../utils/history.js';
import { isRTL, getLang } from '../utils/languages.js';

const MAX_CHARS = 5000;

function IconBtn({ onClick, title, children, active, danger, style = {} }) {
  return (
    <button
      onClick={onClick}
      title={title}
      style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        width: 34, height: 34, borderRadius: 9,
        border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
        background: active ? 'var(--accent-glow)' : 'var(--surface2)',
        color: active ? 'var(--accent2)' : danger ? 'var(--danger)' : 'var(--text2)',
        cursor: 'pointer', transition: 'all 0.18s', flexShrink: 0, ...style,
      }}
      onMouseEnter={e => {
        if (!active) { e.currentTarget.style.borderColor = danger ? 'rgba(224,58,58,0.4)' : 'var(--border-strong)'; e.currentTarget.style.color = danger ? 'var(--danger)' : 'var(--text)'; }
      }}
      onMouseLeave={e => {
        if (!active) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = danger ? 'var(--danger)' : 'var(--text2)'; }
      }}
    >
      {children}
    </button>
  );
}

export function TranslatorCard({ toast, setHistory }) {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('es');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [realtimeMode, setRealtimeMode] = useState(true);
  const [detectedLang, setDetectedLang] = useState(null);
  const [copied, setCopied] = useState(false);
  const [charAnim, setCharAnim] = useState(false);
  const textareaRef = useRef(null);
  const abortRef = useRef(null);
  const debouncedText = useDebounce(sourceText, 450);
  const { speak, stopSpeaking, speaking, startListening, stopListening, listening } = useSpeech();

  // Auto-focus
  useEffect(() => { textareaRef.current?.focus(); }, []);

  const doTranslate = useCallback(async (text, src, tgt) => {
    if (!text.trim() || text.trim().length < 2) { setTranslatedText(''); return; }
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setLoading(true);
    setError('');
    try {
      const result = await translateText({ text, sourceLang: src, targetLang: tgt });
      if (controller.signal.aborted) return;
      setTranslatedText(result.translated_text);
      if (result.detected_language && src === 'auto') {
        setDetectedLang({ code: result.detected_language, name: result.detected_language_name });
      }
      setHistory(addToHistory({
        sourceText: text,
        translatedText: result.translated_text,
        sourceLang: src,
        targetLang: tgt,
        detectedLang: result.detected_language,
      }));
    } catch (e) {
      if (!controller.signal.aborted) { setError(e.message); toast({ message: e.message, type: 'error' }); }
    } finally {
      if (!controller.signal.aborted) setLoading(false);
    }
  }, [toast, setHistory]);

  // Real-time debounced translation
  useEffect(() => {
    if (realtimeMode && debouncedText) doTranslate(debouncedText, sourceLang, targetLang);
    if (!debouncedText) { setTranslatedText(''); setDetectedLang(null); }
  }, [debouncedText, sourceLang, targetLang, realtimeMode]);

  const handleSwap = () => {
    if (sourceLang === 'auto') return;
    const newSrc = targetLang;
    const newTgt = sourceLang;
    const newText = translatedText;
    setSourceLang(newSrc);
    setTargetLang(newTgt);
    setSourceText(newText);
    setTranslatedText(sourceText);
    if (realtimeMode) doTranslate(newText, newSrc, newTgt);
  };

  const handleCopy = async () => {
    if (!translatedText) return;
    await navigator.clipboard.writeText(translatedText);
    setCopied(true);
    toast({ message: 'Copied to clipboard', type: 'success' });
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!translatedText) return;
    const blob = new Blob([`Source (${getLang(sourceLang).name}):\n${sourceText}\n\nTranslation (${getLang(targetLang).name}):\n${translatedText}`], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `translation_${targetLang}_${Date.now()}.txt`;
    a.click();
    toast({ message: 'Translation downloaded', type: 'success' });
  };

  const handleVoiceInput = () => {
    if (listening) { stopListening(); return; }
    const langCode = sourceLang === 'auto' ? 'en-US' : sourceLang + (sourceLang.length === 2 ? '-' + sourceLang.toUpperCase() : '');
    const ok = startListening((transcript, isFinal) => {
      setSourceText(transcript);
      if (isFinal && !realtimeMode) doTranslate(transcript, sourceLang, targetLang);
    }, langCode);
    if (!ok) toast({ message: 'Speech recognition not supported in this browser', type: 'error' });
  };

  const handleSpeak = () => {
    if (speaking) { stopSpeaking(); return; }
    if (!translatedText) return;
    speak(translatedText, targetLang);
  };

  const handleTextChange = (e) => {
    const val = e.target.value;
    if (val.length <= MAX_CHARS) {
      setSourceText(val);
      setCharAnim(true);
      setTimeout(() => setCharAnim(false), 300);
    }
  };

  const charPct = (sourceText.length / MAX_CHARS) * 100;
  const nearLimit = charPct > 80;

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', gap: 0,
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius)',
      boxShadow: 'var(--shadow-lg)',
      backdropFilter: 'blur(24px)',
      overflow: 'hidden',
    }}>

      {/* Language Bar */}
      <div style={{
        display: 'flex', alignItems: 'center',
        padding: '16px 20px',
        borderBottom: '1px solid var(--border)',
        gap: 12, flexWrap: 'wrap',
      }}>
        <LanguageSelector value={sourceLang} onChange={setSourceLang} includeAuto label="From" />

        {/* Swap */}
        <button
          onClick={handleSwap}
          disabled={sourceLang === 'auto'}
          title="Swap languages"
          style={{
            flexShrink: 0, width: 40, height: 40, marginTop: 22,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            border: '1.5px solid var(--border)',
            borderRadius: '50%',
            background: 'var(--surface2)',
            color: sourceLang === 'auto' ? 'var(--text3)' : 'var(--text)',
            cursor: sourceLang === 'auto' ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s',
            opacity: sourceLang === 'auto' ? 0.4 : 1,
          }}
          onMouseEnter={e => { if (sourceLang !== 'auto') { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.background = 'var(--accent-glow)'; e.currentTarget.style.color = 'var(--accent2)'; e.currentTarget.style.transform = 'rotate(180deg)'; } }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.background = 'var(--surface2)'; e.currentTarget.style.color = 'var(--text)'; e.currentTarget.style.transform = 'rotate(0deg)'; }}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M11 3l3 3-3 3M2 6h12M5 13l-3-3 3-3M14 10H2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>

        <LanguageSelector value={targetLang} onChange={setTargetLang} includeAuto={false} label="To" />

        {/* Realtime toggle */}
        <div style={{ marginLeft: 'auto', marginTop: 22, display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 12, color: 'var(--text3)', fontWeight: 500, whiteSpace: 'nowrap' }}>Live</span>
          <button
            onClick={() => setRealtimeMode(m => !m)}
            title={`${realtimeMode ? 'Disable' : 'Enable'} real-time translation`}
            style={{
              width: 44, height: 24, borderRadius: 12,
              background: realtimeMode ? 'var(--accent)' : 'var(--border-strong)',
              border: 'none', cursor: 'pointer',
              position: 'relative', transition: 'background 0.25s',
              flexShrink: 0,
            }}
          >
            <span style={{
              position: 'absolute', top: 3, left: realtimeMode ? 22 : 3,
              width: 18, height: 18, borderRadius: '50%',
              background: 'white',
              boxShadow: '0 1px 4px rgba(0,0,0,0.2)',
              transition: 'left 0.25s cubic-bezier(0.34,1.56,0.64,1)',
              display: 'block',
            }} />
          </button>
        </div>
      </div>

      {/* Panels */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', minHeight: 320 }}>

        {/* Source Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)', position: 'relative' }}>
          {/* Detected badge */}
          {detectedLang && sourceLang === 'auto' && (
            <div style={{
              position: 'absolute', top: 12, left: 16,
              fontSize: 11, fontWeight: 600, letterSpacing: '0.04em',
              color: 'var(--cyan)', background: 'rgba(0,196,180,0.1)',
              border: '1px solid rgba(0,196,180,0.3)',
              borderRadius: 20, padding: '2px 10px',
              animation: 'fadeIn 0.3s both',
            }}>
              Detected: {detectedLang.name}
            </div>
          )}
          <textarea
            ref={textareaRef}
            value={sourceText}
            onChange={handleTextChange}
            placeholder="Type or paste text to translate..."
            dir={isRTL(sourceLang) ? 'rtl' : 'ltr'}
            style={{
              flex: 1, padding: detectedLang ? '44px 20px 16px' : '20px',
              background: 'transparent', border: 'none', outline: 'none',
              fontSize: 16, lineHeight: 1.7,
              color: 'var(--text)', resize: 'none',
              fontFamily: 'var(--font-body)',
            }}
          />

          {/* Source footer */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 8,
            padding: '10px 16px', borderTop: '1px solid var(--border)',
          }}>
            <span style={{
              fontSize: 11, fontWeight: 500,
              color: nearLimit ? 'var(--danger)' : 'var(--text3)',
              transition: 'color 0.2s',
              animation: charAnim ? 'typewriter 0.2s both' : 'none',
            }}>
              {sourceText.length.toLocaleString()} / {MAX_CHARS.toLocaleString()}
            </span>

            {/* Char bar */}
            <div style={{ flex: 1, height: 3, background: 'var(--border)', borderRadius: 2, overflow: 'hidden' }}>
              <div style={{
                height: '100%', width: `${Math.min(charPct, 100)}%`,
                background: nearLimit ? 'var(--danger)' : 'var(--accent)',
                borderRadius: 2, transition: 'width 0.2s, background 0.2s',
              }} />
            </div>

            <div style={{ display: 'flex', gap: 6, marginLeft: 'auto' }}>
              {/* Voice input */}
              <IconBtn onClick={handleVoiceInput} title={listening ? 'Stop listening' : 'Voice input'} active={listening}>
                {listening ? (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <rect x="4" y="4" width="6" height="6" rx="1" fill="var(--danger)"/>
                  </svg>
                ) : (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <rect x="5" y="1" width="4" height="7" rx="2" stroke="currentColor" strokeWidth="1.3"/>
                    <path d="M2.5 7c0 2.5 2 4.5 4.5 4.5S11.5 9.5 11.5 7M7 11.5V13" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"/>
                  </svg>
                )}
              </IconBtn>

              {/* Clear */}
              {sourceText && (
                <IconBtn onClick={() => { setSourceText(''); setTranslatedText(''); setDetectedLang(null); textareaRef.current?.focus(); }} title="Clear" danger>
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M11 3L3 11M3 3l8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </IconBtn>
              )}

              {/* Manual translate */}
              {!realtimeMode && (
                <button
                  onClick={() => doTranslate(sourceText, sourceLang, targetLang)}
                  disabled={!sourceText.trim() || loading}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 6,
                    padding: '6px 14px', borderRadius: 9,
                    background: 'var(--accent)', color: 'white',
                    border: 'none', cursor: 'pointer',
                    fontSize: 12, fontWeight: 600,
                    opacity: (!sourceText.trim() || loading) ? 0.5 : 1,
                    transition: 'all 0.2s',
                  }}
                >
                  Translate
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Output Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', position: 'relative', background: 'var(--surface2)' }}>
          {/* Loading shimmer */}
          {loading && (
            <div style={{
              position: 'absolute', inset: 0, zIndex: 10,
              background: 'linear-gradient(90deg, transparent, var(--accent-glow), transparent)',
              backgroundSize: '200% 100%',
              animation: 'shimmer 1.2s infinite',
              pointerEvents: 'none', borderRadius: '0 0 0 0',
            }} />
          )}

          <div
            dir={isRTL(targetLang) ? 'rtl' : 'ltr'}
            style={{
              flex: 1, padding: '20px',
              fontSize: 16, lineHeight: 1.7,
              color: translatedText ? 'var(--text)' : 'var(--text3)',
              fontFamily: 'var(--font-body)',
              whiteSpace: 'pre-wrap', wordBreak: 'break-word',
              overflowY: 'auto',
            }}
          >
            {loading && !translatedText ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, paddingTop: 4 }}>
                {[100, 85, 92, 60].map((w, i) => (
                  <div key={i} style={{
                    height: 16, width: `${w}%`, borderRadius: 8,
                    background: 'var(--border)',
                    animation: `shimmer 1.5s ${i * 0.15}s infinite`,
                    backgroundImage: 'linear-gradient(90deg, var(--border), var(--border-strong), var(--border))',
                    backgroundSize: '200% 100%',
                  }} />
                ))}
              </div>
            ) : translatedText ? (
              <span style={{ animation: 'fadeIn 0.3s both' }}>{translatedText}</span>
            ) : (
              <span style={{ fontStyle: 'italic', fontSize: 15 }}>Translation will appear here...</span>
            )}
          </div>

          {/* Output footer */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 8,
            padding: '10px 16px', borderTop: '1px solid var(--border)',
          }}>
            {translatedText && (
              <>
                <span style={{ fontSize: 11, color: 'var(--text3)', fontWeight: 500 }}>
                  {translatedText.length.toLocaleString()} chars
                </span>
                <div style={{ flex: 1 }} />

                {/* Speak */}
                <IconBtn onClick={handleSpeak} title={speaking ? 'Stop speaking' : 'Listen to translation'} active={speaking}>
                  {speaking ? (
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <rect x="3" y="3" width="3" height="8" rx="1" fill="currentColor"/>
                      <rect x="8" y="3" width="3" height="8" rx="1" fill="currentColor"/>
                    </svg>
                  ) : (
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <path d="M2 5.5h2L7 3v8L4 8.5H2z" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round"/>
                      <path d="M9 5c.8.5 1.3 1.4 1.3 2.5S9.8 9.5 9 10" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"/>
                      <path d="M10.5 3.5c1.5 1 2.5 2.7 2.5 4.5s-1 3.5-2.5 4.5" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"/>
                    </svg>
                  )}
                </IconBtn>

                {/* Copy */}
                <IconBtn onClick={handleCopy} title="Copy translation" active={copied}>
                  {copied ? (
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <path d="M2 7l4 4 6-6" stroke="var(--success)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ) : (
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <rect x="5" y="1" width="8" height="8" rx="1.5" stroke="currentColor" strokeWidth="1.3"/>
                      <path d="M9 9v2.5A1.5 1.5 0 0 1 7.5 13h-6A1.5 1.5 0 0 1 0 11.5v-6A1.5 1.5 0 0 1 1.5 4H4" stroke="currentColor" strokeWidth="1.3"/>
                    </svg>
                  )}
                </IconBtn>

                {/* Download */}
                <IconBtn onClick={handleDownload} title="Download translation">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M7 1v8M4 6l3 3 3-3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M1 10v1.5A1.5 1.5 0 0 0 2.5 13h9a1.5 1.5 0 0 0 1.5-1.5V10" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
                  </svg>
                </IconBtn>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
