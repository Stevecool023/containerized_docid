/**
 * Flask API base URL for Next.js server-side routes (API route handlers).
 * In Docker, set BACKEND_API_URL as a **Compose build arg** (e.g. http://docid_core_backend:5001/api/v1). Next.js
 * inlines server env at `next build`; `.env*` files are not in the image (see .dockerignore).
 */
export const BACKEND_API_URL = (
  process.env.BACKEND_API_URL ||
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  'http://127.0.0.1:5001/api/v1'
).replace(/\/$/, '');
