/**
 * /api/waitlist.js: Server-side proxy for waitlist form submissions
 *
 * Receives form data from the browser (no auth needed, it's a public signup form),
 * then forwards to RealStack Ops API using a shared WAITLIST_API_KEY header.
 * This replaces the old Google Sheets integration.
 *
 * Env vars required (set in Vercel → Settings → Environment Variables):
 *   WAITLIST_API_KEY: Shared secret matching the value in the Ops Vercel project
 */

// In-memory per-IP rate limit (per lambda instance, good enough to stop
// naive flooding of the Ops waitlist through this public proxy).
const RATE_WINDOW_MS = 10 * 60 * 1000 // 10 min
const RATE_MAX = 5
const rateMap = new Map()
function rateLimited(ip) {
  const now = Date.now()
  if (rateMap.size > 5000) rateMap.clear() // cap memory
  const entry = rateMap.get(ip)
  if (!entry || now - entry.start > RATE_WINDOW_MS) {
    rateMap.set(ip, { start: now, count: 1 })
    return false
  }
  entry.count++
  return entry.count > RATE_MAX
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown'
  if (rateLimited(ip)) {
    res.setHeader('Retry-After', '600')
    return res.status(429).json({ error: 'Too many requests. Please try again later.' })
  }

  const { email, firstName, lastName, phone, company } = req.body || {}

  // Honeypot: real users never see or fill this field. Bots do. Pretend success.
  if (company && String(company).trim()) {
    return res.status(200).json({ ok: true })
  }

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
