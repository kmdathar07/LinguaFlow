import { useState, useCallback } from 'react';

let id = 0;

export function useToast() {
  const [toasts, setToasts] = useState([]);

  const toast = useCallback(({ message, type = 'info', duration = 3000 }) => {
    const tid = ++id;
    setToasts(prev => [...prev, { id: tid, message, type, exiting: false }]);
    setTimeout(() => {
      setToasts(prev => prev.map(t => t.id === tid ? { ...t, exiting: true } : t));
      setTimeout(() => setToasts(prev => prev.filter(t => t.id !== tid)), 350);
    }, duration);
  }, []);

  const dismiss = useCallback((tid) => {
    setToasts(prev => prev.map(t => t.id === tid ? { ...t, exiting: true } : t));
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== tid)), 350);
  }, []);

  return { toasts, toast, dismiss };
}
