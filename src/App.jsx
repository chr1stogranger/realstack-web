import { useState } from 'react'

const LINKS = {
  blueprint: 'https://blueprint.realstack.app?theme=dark',
  pricepoint: 'https://blueprint.realstack.app?mode=pricepoint&theme=dark',
  ops: 'https://ops.realstack.app',
  calendly: 'https://calendly.com/chrisgranger',
  substack: 'https://chrisgranger.substack.com',
  linkedin: 'https://www.linkedin.com/in/christogranger/',
}

/* ─── Icon components (Feather-style, 24x24) ─── */
const I = {
  Grid: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>,
  Target: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>,
  TrendUp: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>,
  Layers: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>,
  Users: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
  Home: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>,
  Briefcase: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>,
  Bolt: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>,
  Shield: (p) => <svg width={p.s||20} height={p.s||20} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>,
  ArrowRight: (p) => <svg width={p.s||16} height={p.s||16} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>,
  Menu: () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>,
  X: () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>,
}

/* ─── Logo SVG ─── */
const LogoIcon = ({ size = 32 }) => (
  <svg viewBox="0 0 100 100" fill="none" style={{width:size,height:size,borderRadius:size*0.22,overflow:'hidden',flexShrink:0}}>
    <defs><linearGradient id="rs-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#6366F1"/><stop offset="100%" stopColor="#3B82F6"/></linearGradient></defs>
    <rect width="100" height="100" fill="url(#rs-bg)"/>
    <polygon points="50,12 8,30 50,25 92,30" fill="rgba(255,255,255,0.95)"/>
    <polygon points="50,25 92,30 92,34 50,29" fill="rgba(255,255,255,0.48)"/>
    <polygon points="50,25 8,30 8,34 50,29" fill="rgba(255,255,255,0.68)"/>
    <polygon points="8,38 50,33 92,38 50,43" fill="rgba(255,255,255,0.90)"/>
    <polygon points="8,38 50,43 50,46 8,41" fill="rgba(255,255,255,0.58)"/>
    <polygon points="50,43 92,38 92,41 50,46" fill="rgba(255,255,255,0.40)"/>
    <polygon points="8,52 50,47 92,52 50,57" fill="rgba(255,255,255,0.70)"/>
    <polygon points="8,52 50,57 50,60 8,55" fill="rgba(255,255,255,0.45)"/>
    <polygon points="50,57 92,52 92,55 50,60" fill="rgba(255,255,255,0.28)"/>
    <polygon points="8,66 50,61 92,66 50,71" fill="rgba(255,255,255,0.50)"/>
    <polygon points="8,66 50,71 50,74 8,69" fill="rgba(255,255,255,0.32)"/>
    <polygon points="50,71 92,66 92,69 50,74" fill="rgba(255,255,255,0.18)"/>
    <polygon points="8,80 50,75 92,80 50,85" fill="rgba(255,255,255,0.34)"/>
    <polygon points="8,80 50,85 50,88 8,83" fill="rgba(255,255,255,0.20)"/>
    <polygon points="50,85 92,80 92,83 50,88" fill="rgba(255,255,255,0.10)"/>
  </svg>
)

const products = [
  {
    name: 'Blueprint',
    desc: 'The mortgage calculator that shows every dollar. Payment breakdowns, tax savings, amortization, side-by-side comparisons — built for the conversation between broker and client.',
    icon: <I.Grid s={22} />,
    color: '#6366F1',
    tag: 'Live',
    tagClass: 'tag-live',
    link: LINKS.blueprint,
    cta: 'Try Free',
  },
  {
    name: 'PricePoint',
    desc: 'A gamified real estate price guessing experience. Browse real listings, guess the price, see how close you get. Addictive engagement meets market education.',
    icon: <I.Target s={22} />,
    color: '#06B6D4',
    tag: 'Live',
    tagClass: 'tag-live',
    link: LINKS.pricepoint,
    cta: 'Play Now',
  },
  {
    name: 'Markets',
    desc: 'Real estate prediction markets powered by Kalshi. Bet on home prices, rate movements, and housing policy. Crowd intelligence meets real estate data.',
    icon: <I.TrendUp s={22} />,
    color: '#3B82F6',
    tag: 'Beta',
    tagClass: 'tag-beta',
    link: LINKS.blueprint,
    cta: 'Join Beta',
  },
  {
    name: 'Ops',
    desc: 'Deal management for mortgage professionals. Live pipeline synced with your LOS, Gmail integration, realtor CRM, commission tracking — one dashboard for your entire business.',
    icon: <I.Layers s={22} />,
    color: '#10B981',
    tag: 'Coming Soon',
    tagClass: 'tag-coming',
    link: null,
    cta: 'Waitlist',
  },
]

const audiences = [
  { icon: <I.Users s={24} />, color: '#6366F1', title: 'Loan Officers', desc: 'White-label Blueprint for your clients. Manage your pipeline with Ops. Stand out with technology your competitors don\'t have.' },
  { icon: <I.Home s={24} />, color: '#06B6D4', title: 'Homebuyers', desc: 'See every dollar before you commit. Compare scenarios, understand tax savings, and make the biggest purchase of your life with total clarity.' },
  { icon: <I.Briefcase s={24} />, color: '#10B981', title: 'Real Estate Agents', desc: 'Send clients a Blueprint instead of a rate sheet. PricePoint drives engagement at open houses. Real tools that close deals faster.' },
]

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [email, setEmail] = useState('')
  const [waitlistStatus, setWaitlistStatus] = useState(null)

  const handleWaitlist = (e) => {
    e.preventDefault()
    if (!email) return
    setWaitlistStatus('success')
    setEmail('')
    setTimeout(() => setWaitlistStatus(null), 4000)
  }

  const scrollTo = (id) => {
    setMobileMenuOpen(false)
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <>
      {/* ─── HEADER ─── */}
      <header className="header">
        <div className="container">
          <div className="logo" onClick={() => scrollTo('hero')}>
            <LogoIcon size={30} />
            <span className="logo-text"><span className="real">Real</span><span className="stack">Stack</span></span>
          </div>
          <nav className="nav">
            <a onClick={() => scrollTo('products')}>Products</a>
            <a onClick={() => scrollTo('for-who')}>For Who</a>
            <a onClick={() => scrollTo('about')}>About</a>
            <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer" className="nav-cta">Try Blueprint</a>
          </nav>
          <button className="mobile-menu-btn" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} aria-label="Toggle menu">
            {mobileMenuOpen ? <I.X /> : <I.Menu />}
          </button>
        </div>
        {mobileMenuOpen && (
          <div style={{background:'var(--bg-elevated)',borderBottom:'1px solid var(--border)',padding:'16px 24px',display:'flex',flexDirection:'column',gap:'12px'}}>
            <a onClick={() => scrollTo('products')} style={{color:'var(--text-secondary)',fontSize:'0.9rem',cursor:'pointer'}}>Products</a>
            <a onClick={() => scrollTo('for-who')} style={{color:'var(--text-secondary)',fontSize:'0.9rem',cursor:'pointer'}}>For Who</a>
            <a onClick={() => scrollTo('about')} style={{color:'var(--text-secondary)',fontSize:'0.9rem',cursor:'pointer'}}>About</a>
            <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer" className="btn btn-accent" style={{marginTop:'8px',textAlign:'center'}}>Try Blueprint</a>
          </div>
        )}
      </header>

      {/* ─── HERO ─── */}
      <section className="hero" id="hero">
        <div className="hero-aurora">
          <div className="blob blob-1"></div>
          <div className="blob blob-2"></div>
          <div className="blob blob-3"></div>
        </div>
        <div className="hero-grid"></div>
        <div className="container animate">
          <div className="label" style={{marginBottom:24}}>MORTGAGE TECHNOLOGY PLATFORM</div>
          <h1>The full real estate<br/>stack <span className="gradient">in your pocket.</span></h1>
          <p className="subtitle">Mortgage calculator. Deal management. Prediction markets. Price discovery. Everything a modern mortgage professional needs — in one platform.</p>
          <div className="btn-group" style={{justifyContent:'center'}}>
            <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer" className="btn btn-shimmer btn-lg">Try Blueprint Free</a>
            <a onClick={() => scrollTo('waitlist')} className="btn btn-secondary btn-lg" style={{cursor:'pointer'}}>Join the Waitlist <I.ArrowRight /></a>
          </div>
          <div className="hero-badges">
            <div className="hero-chip"><div className="dot"></div>4 Products Live or In Beta</div>
            <div className="hero-chip"><div className="dot" style={{background:'var(--accent)'}}></div>Built by a Broker</div>
            <div className="hero-chip"><div className="dot" style={{background:'var(--teal)'}}></div>Kalshi Partnership</div>
          </div>
        </div>
      </section>

      {/* ─── STATS ─── */}
      <div className="container animate delay-2">
        <div className="stats-bar">
          <div className="stat-item">
            <div className="stat-value">1,000+</div>
            <div className="stat-label">Loans Closed</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">13yr</div>
            <div className="stat-label">Bay Area Network</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">8</div>
            <div className="stat-label">States Licensed</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">4</div>
            <div className="stat-label">Products</div>
          </div>
        </div>
      </div>

      <div className="glow-divider"></div>

      {/* ─── PRODUCTS ─── */}
      <section id="products">
        <div className="container">
          <div className="section-center">
            <div className="section-label animate">THE STACK</div>
            <h2 className="section-title animate delay-1">Four products. One platform.</h2>
            <p className="section-desc animate delay-2">Each tool solves a real problem in the mortgage workflow. Together, they create an ecosystem no competitor can replicate.</p>
          </div>
          <div className="products-grid">
            {products.map((p, i) => (
              <div key={p.name} className={`product-card animate delay-${i+1}`} style={{'--card-accent': p.color}}>
                <div className="card-icon" style={{background:`${p.color}15`}}>
                  <span style={{color: p.color}}>{p.icon}</span>
                </div>
                <h3>{p.name}</h3>
                <p className="card-desc">{p.desc}</p>
                <div style={{display:'flex',alignItems:'center',gap:12}}>
                  <span className={`card-tag ${p.tagClass}`}>{p.tag}</span>
                  {p.link ? (
                    <a href={p.link} target="_blank" rel="noopener noreferrer" className="btn btn-ghost" style={{padding:'4px 0',fontSize:'0.82rem',color:p.color}}>
                      {p.cta} <I.ArrowRight />
                    </a>
                  ) : (
                    <a onClick={() => scrollTo('waitlist')} className="btn btn-ghost" style={{padding:'4px 0',fontSize:'0.82rem',color:p.color,cursor:'pointer'}}>
                      {p.cta} <I.ArrowRight />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="glow-divider"></div>

      {/* ─── FOR WHO ─── */}
      <section id="for-who">
        <div className="container">
          <div className="section-center">
            <div className="section-label animate">BUILT FOR</div>
            <h2 className="section-title animate delay-1">Technology that serves everyone in the transaction.</h2>
            <p className="section-desc animate delay-2">Whether you originate loans, buy homes, or sell them — RealStack gives you an unfair advantage.</p>
          </div>
          <div className="audience-grid">
            {audiences.map((a, i) => (
              <div key={a.title} className={`audience-card animate delay-${i+1}`}>
                <div className="audience-icon" style={{background:`${a.color}15`}}>
                  <span style={{color: a.color}}>{a.icon}</span>
                </div>
                <h3>{a.title}</h3>
                <p>{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="glow-divider"></div>

      {/* ─── FOUNDER / ABOUT ─── */}
      <section id="about">
        <div className="container">
          <div className="founder-section">
            <div className="animate">
              <div className="section-label">THE BUILDER</div>
              <h2 className="section-title" style={{marginTop:16}}>Built by a broker who closes loans every day.</h2>
              <p style={{color:'var(--text-secondary)',lineHeight:1.7,marginTop:16,fontSize:'0.95rem'}}>
                RealStack isn't a VC-backed experiment from people who've never originated a loan. It's built by Chris Granger — a mortgage broker with 1,000+ loans closed, a 13-year realtor network across the Bay Area, and the daily frustration of using tools that weren't built for how deals actually work.
              </p>
              <p style={{color:'var(--text-secondary)',lineHeight:1.7,marginTop:12,fontSize:'0.95rem'}}>
                Every feature exists because it solved a real problem on a real deal. That's the difference.
              </p>
              <div style={{marginTop:24,display:'flex',gap:12,flexWrap:'wrap'}}>
                <a href={LINKS.substack} target="_blank" rel="noopener noreferrer" className="btn btn-secondary" style={{fontSize:'0.82rem',padding:'8px 18px'}}>Three Point Thursday</a>
                <a href={LINKS.linkedin} target="_blank" rel="noopener noreferrer" className="btn btn-secondary" style={{fontSize:'0.82rem',padding:'8px 18px'}}>LinkedIn</a>
              </div>
            </div>
            <div className="animate delay-2">
              <div className="founder-stats">
                <div className="founder-stat"><div className="value">1,000+</div><div className="label">Loans Closed</div></div>
                <div className="founder-stat"><div className="value">290+</div><div className="label">Five-Star Reviews</div></div>
                <div className="founder-stat"><div className="value">13yr</div><div className="label">Bay Area Network</div></div>
                <div className="founder-stat"><div className="value">8</div><div className="label">States Licensed</div></div>
              </div>
              <div style={{marginTop:16,padding:20,background:'var(--bg-card)',border:'1px solid var(--border)',borderRadius:'var(--radius)',borderLeft:'3px solid var(--accent)'}}>
                <div style={{fontFamily:'var(--mono)',fontSize:'0.65rem',fontWeight:600,textTransform:'uppercase',letterSpacing:'1.5px',color:'var(--accent-light)',marginBottom:8}}>PARTNERSHIP</div>
                <p style={{fontSize:'0.85rem',color:'var(--text-secondary)',lineHeight:1.6}}>RealStack Markets is built in partnership with Kalshi, the first CFTC-regulated prediction market exchange. Real money. Real odds. Real signal.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── WAITLIST CTA ─── */}
      <section className="cta-section" id="waitlist">
        <div className="container animate">
          <div className="label" style={{marginBottom:16}}>EARLY ACCESS</div>
          <h2>The platform is live.<br/>The waitlist is for what's next.</h2>
          <p>Blueprint is free to use today. Join the waitlist to get early access to Ops, white-label LO tools, and platform updates before anyone else.</p>
          <form className="waitlist-form" onSubmit={handleWaitlist}>
            <input type="email" placeholder="you@email.com" value={email} onChange={e => setEmail(e.target.value)} required />
            <button type="submit" className="btn btn-accent" style={{whiteSpace:'nowrap'}}>Join Waitlist</button>
          </form>
          {waitlistStatus === 'success' && (
            <p style={{color:'var(--green)',fontSize:'0.85rem',marginTop:16,fontFamily:'var(--mono)'}}>You're on the list. We'll be in touch.</p>
          )}
          <div style={{marginTop:40,display:'flex',gap:12,justifyContent:'center',flexWrap:'wrap'}}>
            <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer" className="btn btn-white">Try Blueprint Free</a>
            <a href={LINKS.calendly} target="_blank" rel="noopener noreferrer" className="btn btn-secondary">Schedule a Demo</a>
          </div>
        </div>
      </section>

      {/* ─── FOOTER ─── */}
      <footer className="footer">
        <div className="container">
          <div className="footer-grid">
            <div className="footer-brand">
              <div style={{display:'flex',alignItems:'center',gap:10}}>
                <LogoIcon size={24} />
                <span style={{fontSize:'1rem',fontWeight:700,letterSpacing:'-0.03em'}}><span style={{color:'var(--text-primary)'}}>Real</span><span style={{color:'var(--accent)'}}>Stack</span></span>
              </div>
              <p>Mortgage technology platform. Built in the Bay Area by a broker who closes loans every day.</p>
            </div>
            <div className="footer-links">
              <div className="footer-col">
                <h4>Products</h4>
                <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer">Blueprint</a>
                <a href={LINKS.pricepoint} target="_blank" rel="noopener noreferrer">PricePoint</a>
                <a href={LINKS.blueprint} target="_blank" rel="noopener noreferrer">Markets</a>
                <a onClick={() => scrollTo('waitlist')} style={{cursor:'pointer'}}>Ops</a>
              </div>
              <div className="footer-col">
                <h4>Company</h4>
                <a href={LINKS.substack} target="_blank" rel="noopener noreferrer">Newsletter</a>
                <a href={LINKS.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a>
                <a href={LINKS.calendly} target="_blank" rel="noopener noreferrer">Schedule a Call</a>
              </div>
              <div className="footer-col">
                <h4>Legal</h4>
                <a href="https://blueprint.realstack.app/privacy" target="_blank" rel="noopener noreferrer">Privacy</a>
                <a href="https://ops.realstack.app/terms" target="_blank" rel="noopener noreferrer">Terms</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; {new Date().getFullYear()} RealStack. All rights reserved.</p>
            <span className="nmls">NMLS #952015 &middot; NMLS #2179191</span>
          </div>
        </div>
      </footer>
    </>
  )
}
