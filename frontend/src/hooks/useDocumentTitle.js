import { useEffect } from 'react';

const BASE = 'SkyAgent';

export function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} — ${BASE}` : `${BASE} — Passagens Aéreas`;
    return () => {
      document.title = `${BASE} — Passagens Aéreas`;
    };
  }, [title]);
}
