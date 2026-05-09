const HISTORY_KEY = 'linguaflow_history';
const MAX_HISTORY = 50;

export function getHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  } catch {
    return [];
  }
}

export function addToHistory(entry) {
  const history = getHistory();
  const newEntry = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    ...entry,
  };
  const updated = [newEntry, ...history.filter(h =>
    !(h.sourceText === entry.sourceText && h.targetLang === entry.targetLang)
  )].slice(0, MAX_HISTORY);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
  return updated;
}

export function clearHistory() {
  localStorage.removeItem(HISTORY_KEY);
}

export function removeFromHistory(id) {
  const history = getHistory().filter(h => h.id !== id);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  return history;
}
