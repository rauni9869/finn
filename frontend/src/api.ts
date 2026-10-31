// Same-origin by default: Vite proxies /api in development, and FastAPI serves the built app in production.
export const API_BASE: string = import.meta.env.VITE_API_URL ?? '';
