/**
 * /api/waitlist.js — Server-side proxy for waitlist form submissions
 *
 * Receives form data from the browser (no auth needed — it's a public signup form),
 * then forwards to RealStack Ops API using a shared WAITLIST_API_KEY header.
 * This replaces the old Google Sheets integration.
 *
 * Env vars required (set in Vercel → Settings → Environment Variables):
 *   WAITLIST_API_KEY  — Shared secret matching the value in the Ops Vercel project
 */

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { email, firstName, lastName, phone } = req.body || {}

  // Basic validation
  if (!email || typeof email !== 'string') {
    return res.status(400).json({ error: 'Email is required' })
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email) || email.length > 254) {
    return res.status(400).json({ error: 'Invalid email address' })
  }

  const WAITLIST_API_KEY = process.env.WAITLIST_API_KEY

  if (!WAITLIST_API_KEY) {
    console.error('[waitlist] WAITLIST_API_KEY not configured')
    return res.status(500).json({ error: 'Server misconfiguration. Please email chr1stogranger@gmail.com to sign up.' })
  }

  try {
    const response = await fetch('https://ops.realstack.app/api/waitlist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Waitlist-Key': WAITLIST_API_KEY,
      },
      body: JSON.stringify({
        email: email.toLowerCase().trim(),
        firstName: (firstName || '').trim().slice(0, 100),
        lastName: (lastName || '').trim().slice(0, 100),
        phone: (phone || '').trim().slice(0, 30),
        source: 'realstack.app',
        timestamp: new Date().toISOString(),
      }),
    })

    if (!response.ok) {
      const j = await response.json().catch(() => ({}))
      console.error('[waitlist] Ops API error:', response.status, j)
      return res.status(502).json({ error: 'Could not save to waitlist. Please try again.' })
    }

    return res.status(200).json({ ok: true, message: 'Added to waitlist' })
  } catch (err) {
    console.error('[waitlist] Fetch error:', err.message)
    return res.status(500).json({ error: 'Server error. Please try again.' })
  }
}
