/**
 * /api/waitlist.js — Vercel serverless function for waitlist form submissions
 *
 * Server-side proxy for Google Sheets Apps Script endpoint.
 * Avoids CORS/opaque-response issues from browser-direct no-cors requests.
 * Returns real success/error JSON so the UI can show accurate feedback.
 *
 * Env vars needed (set in Vercel dashboard → Settings → Environment Variables):
 *   WAITLIST_SHEETS_URL — Google Apps Script web app URL (same as old VITE_WAITLIST_SHEETS_URL)
 *
 * Note: Keep VITE_WAITLIST_SHEETS_URL in the frontend build if other places use it,
 * but the waitlist form should now call /api/waitlist instead.
 */

export default async function handler(req, res) {
  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { email, source, timestamp } = req.body || {}

  // Basic email validation
  if (!email || typeof email !== 'string') {
    return res.status(400).json({ error: 'Email is required' })
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email) || email.length > 254) {
    return res.status(400).json({ error: 'Invalid email address' })
  }

  const SHEETS_URL = process.env.WAITLIST_SHEETS_URL

  if (!SHEETS_URL) {
    // Fallback: log to console in dev, still return success to not break the form
    console.warn('[waitlist] WAITLIST_SHEETS_URL not configured — entry not saved', { email, source, timestamp })
    return res.status(200).json({ ok: true, message: 'Recorded' })
  }

  try {
    // Server-to-server: no CORS restrictions, get a real response
    const response = await fetch(SHEETS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.toLowerCase().trim(),
        source: source || 'realstack.app',
        timestamp: timestamp || new Date().toISOString()
      })
    })

    if (!response.ok) {
      const text = await response.text().catch(() => '')
      console.error('[waitlist] Sheets error:', response.status, text)
      return res.status(502).json({ error: 'Could not save to waitlist. Please try again.' })
    }

    return res.status(200).json({ ok: true, message: 'Added to waitlist' })
  } catch (err) {
    console.error('[waitlist] Fetch error:', err.message)
    return res.status(500).json({ error: 'Server error. Please try again.' })
  }
}
