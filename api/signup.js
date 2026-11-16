/**
 * /api/signup.js: Server-side proxy for the "Start free trial" form.
 *
 * Forwards { name, email, phone, plan } to RealStack Ops, which emails a
 * confirmation link; clicking it creates the loan officer's workspace and
 * starts the 14-day trial (Ops api/_signupCore.js). Same shared key and
 * origin rules as /api/waitlist.
 *
 * Env vars required (set in Vercel → Settings → Environment Variables):
 *   WAITLIST_API_KEY: Shared secret matching the value in the Ops Vercel project
 */

const ALLOWED_ORIGINS = new Set(['https://www.realstack.app', 'https://realstack.app'])
const PLANS = new Set(['founder', 'ops_monthly', 'ops_yearly', 'team', 'blueprint'])
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

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
  // Every browser sends Origin on a POST, so none (or a foreign one) is a script.
  const origin = req.headers.origin
  if (!origin || !ALLOWED_ORIGINS.has(origin)) {
    return res.status(403).json({ error: 'Forbidden' })
  }

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown'
  if (rateLimited(ip)) {
    res.setHeader('Retry-After', '600')
    return res.status(429).json({ error: 'Too many requests. Please try again later.' })
  }

  const { email, name, phone, plan, company } = req.body || {}
  // Honeypot: real people never see or fill this field. Pretend success.
  if (company && String(company).trim()) {
    return res.status(200).json({ ok: true })
  }

  const str = (v) => (typeof v === 'string' ? v.trim() : '')
  if (!email || typeof email !== 'string' || !emailRegex.test(email) || email.length > 254) {
    return res.status(400).json({ error: 'Enter a valid email address.' })
  }
  if (str(name).length < 2) {
    return res.status(400).json({ error: 'Enter your name.' })
  }

  const WAITLIST_API_KEY = process.env.WAITLIST_API_KEY
  if (!WAITLIST_API_KEY) {
    console.error('[signup] WAITLIST_API_KEY not configured')
    return res.status(503).json({ error: 'Signup is not available right now.' })
  }

  try {
    const response = await fetch('https://ops.realstack.app/api/waitlist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Waitlist-Key': WAITLIST_API_KEY,
        'X-Visitor-IP': ip,
      },
      body: JSON.stringify({
        action: 'signup',
        email: email.toLowerCase().trim(),
        name: str(name).slice(0, 120),
        phone: str(phone).slice(0, 30),
        plan: PLANS.has(plan) ? plan : 'ops_monthly',
      }),
    })
    const j = await response.json().catch(() => ({}))
    if (!response.ok) {
      console.error('[signup] Ops API error:', response.status)
      return res.status(response.status === 429 ? 429 : 502).json({ error: j.error || 'Could not start your trial. Please try again.' })
    }
    return res.status(200).json({ ok: true })
  } catch (err) {
    console.error('[signup] Fetch error:', err.message)
    return res.status(500).json({ error: 'Server error. Please try again.' })
  }
}
