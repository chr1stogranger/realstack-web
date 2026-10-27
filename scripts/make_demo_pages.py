# Writes public/demo/{ops,blueprint,together}/index.html from one template.
# Run from the repo root: python3 scripts/make_demo_pages.py .
# Each folder also holds wide.mp4 / tall.mp4 (16:9 and 9:16, 1080p) and
# poster.jpg / poster-tall.jpg; public/demo/demo.js picks the shape.
import sys, html
ROOT = sys.argv[1]
CAL = 'https://calendly.com/chrisgranger'
PAGES = {
  'ops': dict(
    title='RealStack Ops Demo', name='RealStack Ops', secs=48,
    h1='RealStack Ops in 48 seconds',
    sub='The mortgage CRM built by a loan officer. Your live pipeline on one screen, status updates in one click, every condition with an owner, refi alerts on past clients, and follow-up on autopilot.',
    og='RealStack Ops: your whole book on one screen. The mortgage CRM built by a loan officer.',
    ctas=[('Claim a founder spot', '/#pricing', True), ('Book a demo', CAL, False)],
    note='Founding member offer: Ops + Blueprint for $99/mo, locked in for life. First 60 days free.'),
  'blueprint': dict(
    title='Mortgage Blueprint Demo', name='Mortgage Blueprint', secs=59,
    h1='Mortgage Blueprint in 59 seconds',
    sub='The real payment, every dollar to close, what you qualify for, what you can actually afford, the tax savings nobody tells you about, and PricePoint to learn your market. Know before you buy.',
    og='Mortgage Blueprint: know before you buy. Payment, cash to close, qualification, affordability and tax savings.',
    ctas=[('Download on the App Store', 'https://apps.apple.com/us/app/mortgage-blueprint/id6773117288', True), ('Try it in your browser', 'https://blueprint.realstack.app', False)],
    note='Free for homebuyers. iPhone and web.'),
  'together': dict(
    title='RealStack Demo', name='Blueprint + Ops', secs=43,
    h1='RealStack in 43 seconds',
    sub='Mortgage Blueprint for your clients, RealStack Ops for you. One stack from first scenario to funded loan.',
    og='Mortgage Blueprint for your clients, RealStack Ops for you. One stack from first scenario to funded loan.',
    ctas=[('See pricing', '/#pricing', True), ('Book a demo', CAL, False)],
    note=None),
}
NAV = [('ops', 'RealStack Ops'), ('blueprint', 'Mortgage Blueprint'), ('together', 'Together')]

CSS = """
      :root {
        --bg-base: #0a1120; --accent: #3B6BF5; --accent-light: #6E90FF; --accent-deep: #2B4FCE;
        --text-primary: #EDEDED; --text-secondary: #A1A1A1; --text-muted: #8A8A8A;
        --border: rgba(255,255,255,0.08); --border-hover: rgba(255,255,255,0.14);
        --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --mono: 'Geist Mono', 'SF Mono', monospace;
      }
      *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: var(--font); color: var(--text-primary); line-height: 1.6;
        background: radial-gradient(1200px 600px at 50% -10%, rgba(59,107,245,0.22), transparent 70%), var(--bg-base);
        min-height: 100vh; -webkit-font-smoothing: antialiased; display: flex; flex-direction: column;
      }
      a { color: inherit; text-decoration: none; }
      header { max-width: 1100px; width: 100%; margin: 0 auto; padding: 24px 16px; }
      .logo { font-weight: 800; font-size: 1.25rem; letter-spacing: -0.04em; }
      .logo span { color: var(--accent-light); }
      main { flex: 1; max-width: 1100px; width: 100%; margin: 0 auto; padding: 16px 16px 64px; text-align: center; }
      .overline { font-family: var(--mono); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent-light); }
      h1 { font-size: clamp(2rem, 5vw, 3.25rem); line-height: 1.1; letter-spacing: -0.04em; margin: 12px 0; }
      .sub { color: var(--text-secondary); font-size: 1.05rem; max-width: 620px; margin: 0 auto 32px; }
      .player {
        margin: 0 auto; border-radius: 16px; overflow: hidden; border: 1px solid var(--border-hover);
        box-shadow: 0 30px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(59,107,245,0.15);
        background: #0d1524; aspect-ratio: 16 / 9; max-width: 1000px;
      }
      .player.tall { aspect-ratio: 9 / 16; max-width: 380px; }
      video { display: block; width: 100%; height: 100%; object-fit: cover; }
      .ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 32px; }
      .btn { display: inline-block; padding: 12px 28px; border-radius: 9999px; font-weight: 600; font-size: 0.95rem; }
      .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent-deep)); color: #fff; }
      .btn-primary:hover { filter: brightness(1.1); }
      .btn-secondary { border: 1px solid var(--border-hover); color: var(--text-primary); }
      .btn-secondary:hover { border-color: var(--accent); color: var(--accent-light); }
      .note { color: var(--text-muted); font-size: 0.85rem; margin-top: 16px; }
      .more { margin-top: 48px; }
      .more .overline { color: var(--text-muted); }
      .more nav { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 12px; }
      .more a { padding: 7px 16px; border-radius: 9999px; border: 1px solid var(--border); color: var(--text-secondary); font-size: 0.85rem; font-weight: 600; }
      .more a:hover { color: var(--text-primary); border-color: var(--border-hover); }
      .more a[aria-current] { color: #fff; border-color: var(--accent); background: rgba(59,107,245,0.18); }
      footer { padding: 24px 16px; text-align: center; color: var(--text-muted); font-size: 0.8rem; }
      a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }"""

def page(key, p):
    e = html.escape
    url = f'https://www.realstack.app/demo/{key}'
    base = f'/demo/{key}'
    ctas = '\n        '.join(
        f'<a class="btn {"btn-primary" if pri else "btn-secondary"}" href="{e(href)}"'
        + ('' if href.startswith('/') else ' target="_blank" rel="noopener noreferrer"') + f'>{e(label)}</a>'
        for label, href, pri in p['ctas'])
    note = f'\n      <p class="note">{e(p["note"])}</p>' if p['note'] else ''
    nav = '\n          '.join(
        f'<a href="/demo/{k}"' + (' aria-current="page"' if k == key else '') + f'>{e(n)}</a>' for k, n in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="16x16 32x32" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{e(p['og'])}" />
    <meta name="theme-color" content="#0a1120" />
    <meta property="og:title" content="{e(p['h1'])}" />
    <meta property="og:description" content="{e(p['og'])}" />
    <meta property="og:type" content="video.other" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{url}/poster.jpg" />
    <meta property="og:image:width" content="1920" />
    <meta property="og:image:height" content="1080" />
    <meta property="og:video" content="{url}/wide.mp4" />
    <meta property="og:video:type" content="video/mp4" />
    <meta property="og:video:width" content="1920" />
    <meta property="og:video:height" content="1080" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{e(p['h1'])}" />
    <meta name="twitter:description" content="{e(p['og'])}" />
    <meta name="twitter:image" content="{url}/poster.jpg" />
    <link rel="canonical" href="{url}" />
    <title>{e(p['title'])}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Geist+Mono:wght@500;600&display=swap" rel="stylesheet" />
    <!-- Generated by scripts/make_demo_pages.py; edit that, not this file.
         Standalone static page; tokens mirror src/App.css :root. -->
    <style>{CSS}
    </style>
  </head>
  <body>
    <header>
      <a class="logo" href="/">Real<span>Stack</span></a>
    </header>
    <main>
      <p class="overline">Product demo &middot; {e(p['name'])}</p>
      <h1>{e(p['h1'])}</h1>
      <p class="sub">{e(p['sub'])}</p>
      <div class="player" data-film>
        <video src="{base}/wide.mp4" poster="{base}/poster.jpg"
          data-wide="{base}/wide.mp4" data-wide-poster="{base}/poster.jpg"
          data-tall="{base}/tall.mp4" data-tall-poster="{base}/poster-tall.jpg"
          controls muted autoplay loop playsinline preload="metadata" aria-label="{e(p['name'])} product film"></video>
      </div>
      <div class="ctas">
        {ctas}
      </div>{note}
      <div class="more">
        <p class="overline">More demos</p>
        <nav aria-label="Product demos">
          {nav}
        </nav>
      </div>
    </main>
    <footer>RealStack &middot; Built by Chris Granger, NMLS 952015</footer>
    <script src="/demo/demo.js"></script>
  </body>
</html>
'''

for k, p in PAGES.items():
    open(f'{ROOT}/public/demo/{k}/index.html', 'w').write(page(k, p))
print('ok')
