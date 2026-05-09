import React from 'react';

export function BackgroundOrbs() {
  return (
    <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', overflow: 'hidden', zIndex: 0 }}>
      <div style={{
        position: 'absolute', top: '-15%', left: '-10%',
        width: 600, height: 600,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(79,47,219,0.12) 0%, transparent 70%)',
        animation: 'orbFloat1 18s ease-in-out infinite',
        filter: 'blur(40px)',
      }} />
      <div style={{
        position: 'absolute', bottom: '-20%', right: '-5%',
        width: 700, height: 700,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(0,196,180,0.1) 0%, transparent 70%)',
        animation: 'orbFloat2 22s ease-in-out infinite',
        filter: 'blur(50px)',
      }} />
      <div style={{
        position: 'absolute', top: '40%', left: '50%',
        width: 400, height: 400,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(124,92,252,0.06) 0%, transparent 70%)',
        animation: 'orbFloat1 28s ease-in-out infinite reverse',
        filter: 'blur(30px)',
      }} />
    </div>
  );
}
