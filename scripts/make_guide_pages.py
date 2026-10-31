# Writes public/guides/{index,loan-officer/index,borrower/index}.html.
# Run from the repo root: python3 scripts/make_guide_pages.py .
#
# Public copies of the in-app guides, so loan officers thinking about
# RealStack can see the whole flow, and LOs can send borrowers a link:
#   /guides               How it works, lead to funded loan (two lanes)
#   /guides/loan-officer  Ops Help Center "Lead to close" (loan-pipeline
#                         src/components/HelpCenter.jsx, docs/LO-MANUAL.md)
#   /guides/borrower      Ops Help Center "Borrower guide" (mortgage-blueprint
#                         docs/BORROWER-MANUAL.md). Ops links borrowers here.
# Change the in-app guide and this file together.
# Screenshots in public/guides/img come from the Ops Test book (made-up
# clients) and a signed-out Blueprint, so no real client ever appears.
# Copy markup: **bold**; everything else is escaped.
import sys, html, os, re

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
CAL = 'https://calendly.com/chrisgranger'
BP = 'https://blueprint.realstack.app'
APP_STORE = 'https://apps.apple.com/us/app/mortgage-blueprint/id6773117288'
BASE = 'https://www.realstack.app'

def md(s):
    s = html.escape(s, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)

CSS = """
      :root {
        --bg-base: #0a1120; --bg-card: #121c30; --bg-elevated: #0d1524;
        --accent: #3B6BF5; --accent-light: #6E90FF; --accent-deep: #2B4FCE; --green: #12a150; --teal: #38c6c6;
        --text-primary: #EDEDED; --text-secondary: #A1A1A1; --text-muted: #8A8A8A;
        --border: rgba(255,255,255,0.08); --border-hover: rgba(255,255,255,0.14);
        --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --mono: 'Geist Mono', 'SF Mono', monospace;
      }
      *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: var(--font); color: var(--text-primary); line-height: 1.65;
        background: radial-gradient(1200px 600px at 50% -10%, rgba(59,107,245,0.20), transparent 70%), var(--bg-base);
        min-height: 100vh; -webkit-font-smoothing: antialiased; display: flex; flex-direction: column;
      }
      a { color: inherit; text-decoration: none; }
      header { max-width: 1100px; width: 100%; margin: 0 auto; padding: 24px 16px; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
      .logo { font-weight: 800; font-size: 1.25rem; letter-spacing: -0.04em; }
      .logo span { color: var(--accent-light); }
      .tabs { display: flex; gap: 6px; flex-wrap: wrap; }
      .tabs a { padding: 7px 14px; border-radius: 9999px; border: 1px solid var(--border); color: var(--text-secondary); font-size: 0.85rem; font-weight: 600; }
      .tabs a:hover { color: var(--text-primary); border-color: var(--border-hover); }
      .tabs a[aria-current] { color: #fff; border-color: var(--accent); background: rgba(59,107,245,0.18); }
      main { flex: 1; max-width: 1100px; width: 100%; margin: 0 auto; padding: 16px 16px 72px; }
      .hero { text-align: center; max-width: 760px; margin: 0 auto 48px; }
      .overline { font-family: var(--mono); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent-light); }
      h1 { font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.1; letter-spacing: -0.04em; margin: 12px 0; text-wrap: balance; }
      h2 { font-size: clamp(1.35rem, 3vw, 1.75rem); line-height: 1.2; letter-spacing: -0.03em; margin-bottom: 12px; text-wrap: balance; }
      h3 { font-size: 1.05rem; letter-spacing: -0.01em; margin-bottom: 6px; }
      .sub { color: var(--text-secondary); font-size: 1.05rem; }
      p { color: var(--text-secondary); }
      p + p { margin-top: 10px; }
      strong { color: var(--text-primary); font-weight: 600; }
      .btn { display: inline-block; padding: 12px 26px; border-radius: 9999px; font-weight: 600; font-size: 0.95rem; }
      .btn-primary { background: linear-gradient(135deg, var(--accent), var(--accent-deep)); color: #fff; }
      .btn-primary:hover { filter: brightness(1.1); }
      .btn-secondary { border: 1px solid var(--border-hover); color: var(--text-primary); }
      .btn-secondary:hover { border-color: var(--accent); color: var(--accent-light); }
      .ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 28px; }
      /* Guide body: TOC rail + article */
      .guide { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 40px; align-items: start; }
      .toc { position: sticky; top: 24px; display: flex; flex-direction: column; gap: 2px; }
      .toc .overline { color: var(--text-muted); margin-bottom: 8px; }
      .toc a { color: var(--text-secondary); font-size: 0.88rem; padding: 5px 10px; border-radius: 8px; }
      .toc a:hover { color: var(--text-primary); background: rgba(255,255,255,0.04); }
      .step { padding: 28px 0; border-top: 1px solid var(--border); scroll-margin-top: 16px; max-width: 720px; }
      .step:first-child { border-top: 0; padding-top: 0; }
      .num { font-family: var(--mono); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; color: var(--accent-light); margin-bottom: 6px; display: block; }
      figure { margin-top: 18px; }
      figure img { display: block; width: 100%; height: auto; border-radius: 14px; border: 1px solid var(--border-hover); box-shadow: 0 24px 60px rgba(0,0,0,0.4); }
      figure.phone img { max-width: 300px; }
      figcaption { color: var(--text-muted); font-size: 0.8rem; margin-top: 8px; }
      .callout { margin-top: 16px; padding: 14px 16px; border-radius: 12px; background: var(--bg-card); border: 1px solid var(--border); }
      .callout p { color: var(--text-secondary); font-size: 0.92rem; }
      /* How it works: two lanes per stage */
      .flow { display: flex; flex-direction: column; gap: 14px; }
      .lane-head { display: grid; grid-template-columns: 200px 1fr 1fr; gap: 14px; padding: 0 4px; }
      .lane-head span { font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); }
      .stage { display: grid; grid-template-columns: 200px 1fr 1fr; gap: 14px; align-items: stretch; }
      .stage-name { padding: 16px 4px; }
      .stage-name h3 { font-size: 1.1rem; }
      .cell { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 16px 18px; }
      .cell .who { display: none; font-family: var(--mono); font-size: 0.66rem; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px; }
      .cell.lo { border-left: 3px solid var(--accent); }
      .cell.borrower { border-left: 3px solid var(--teal); }
      .cell.lo .who { color: var(--accent-light); }
      .cell.borrower .who { color: var(--teal); }
      .cell p { font-size: 0.92rem; }
      .cell.empty { background: transparent; border-style: dashed; }
      .player { margin: 0 auto; border-radius: 16px; overflow: hidden; border: 1px solid var(--border-hover); box-shadow: 0 30px 80px rgba(0,0,0,0.45); background: #0d1524; aspect-ratio: 16 / 9; max-width: 900px; }
      .player.tall { aspect-ratio: 9 / 16; max-width: 360px; }
      video { display: block; width: 100%; height: 100%; object-fit: cover; }
      .block { margin-top: 64px; }
      .center { text-align: center; }
      .cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 24px; }
      .card { display: block; background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 22px; }
      .card:hover { border-color: var(--accent); }
      .card p { font-size: 0.92rem; margin-top: 6px; }
      .card .go { display: inline-block; margin-top: 12px; color: var(--accent-light); font-weight: 600; font-size: 0.9rem; }
      footer { padding: 24px 16px; text-align: center; color: var(--text-muted); font-size: 0.8rem; }
      a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
      @media (max-width: 860px) {
        .guide { grid-template-columns: minmax(0, 1fr); gap: 8px; }
        .toc { position: static; flex-direction: row; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
        .toc .overline { width: 100%; margin-bottom: 2px; }
        .toc a { border: 1px solid var(--border); border-radius: 9999px; font-size: 0.8rem; }
        .lane-head { display: none; }
        .stage { grid-template-columns: minmax(0, 1fr); gap: 8px; }
        .stage-name { padding: 8px 0 0; }
        .cell .who { display: block; }
        .cell.empty { display: none; }
        .cards { grid-template-columns: minmax(0, 1fr); }
      }
"""

TABS = [('', 'How it works'), ('loan-officer', 'For loan officers'), ('borrower', 'For borrowers')]

def page(slug, title, desc, body, film=False):
    path = f'/guides/{slug}' if slug else '/guides'
    tabs = '\n'.join(
        f'        <a href="{"/guides/" + s if s else "/guides"}"{" aria-current=\"page\"" if s == slug else ""}>{html.escape(t)}</a>'
        for s, t in TABS)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="16x16 32x32" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{html.escape(desc)}" />
    <meta name="theme-color" content="#0a1120" />
    <meta property="og:title" content="{html.escape(title)}" />
    <meta property="og:description" content="{html.escape(desc)}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{BASE}{path}" />
    <meta property="og:image" content="{BASE}/og-image.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(title)}" />
    <meta name="twitter:description" content="{html.escape(desc)}" />
    <link rel="canonical" href="{BASE}{path}" />
    <title>{html.escape(title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Geist+Mono:wght@500;600&display=swap" rel="stylesheet" />
    <!-- Generated by scripts/make_guide_pages.py; edit that, not this file. -->
    <style>{CSS}    </style>
  </head>
  <body>
    <header>
      <a class="logo" href="/">Real<span>Stack</span></a>
      <nav class="tabs" aria-label="Guides">
{tabs}
      </nav>
    </header>
    <main>
{body}
    </main>
    <footer>RealStack &middot; Built by Chris Granger, NMLS 952015 &middot; Xpert Home Lending, Inc. NMLS 2179191</footer>
{'    <script src="/demo/demo.js"></script>' if film else ''}
  </body>
</html>
"""

def guide_body(overline, h1, sub, steps, ctas, numbered=True):
    toc = '\n'.join(f'          <a href="#{s["id"]}">{html.escape(s["title"])}</a>' for s in steps)
    out = []
    for i, s in enumerate(steps, 1):
        paras = '\n'.join(f'            <p>{md(p)}</p>' for p in s['body'])
        num = f'<span class="num">STEP {i:02d}</span>' if numbered and s.get('step', True) else ''
        fig = ''
        if s.get('img'):
            cls = ' class="phone"' if s.get('phone') else ''
            fig = (f'\n            <figure{cls}><img src="/guides/img/{s["img"]}" alt="{html.escape(s["alt"])}" loading="lazy" />'
                   f'<figcaption>{html.escape(s["caption"])}</figcaption></figure>')
        call = ''
        if s.get('callout'):
            call = '\n            <div class="callout">' + ''.join(f'<p>{md(c)}</p>' for c in s['callout']) + '</div>'
        out.append(f'          <section class="step" id="{s["id"]}">\n            {num}<h2>{html.escape(s["title"])}</h2>\n{paras}{call}{fig}\n          </section>')
    cta = '\n'.join(f'        <a class="btn {"btn-primary" if p else "btn-secondary"}" href="{u}"{" target=\"_blank\" rel=\"noopener noreferrer\"" if u.startswith("http") else ""}>{html.escape(t)}</a>' for t, u, p in ctas)
    return f"""      <div class="hero">
        <p class="overline">{html.escape(overline)}</p>
        <h1>{html.escape(h1)}</h1>
        <p class="sub">{md(sub)}</p>
      </div>
      <div class="guide">
        <nav class="toc" aria-label="On this page">
          <p class="overline">On this page</p>
{toc}
        </nav>
        <article>
{chr(10).join(out)}
        </article>
      </div>
      <div class="ctas">
{cta}
      </div>"""

# ── For loan officers (mirrors Ops Help Center "Lead to close") ─────────────
LO_STEPS = [
  dict(id='intake', title='The lead comes in', img='ops-leads.webp', alt='Ops Leads tab', caption='Leads, from the Ops Test book. Every client shown is made up.', body=[
    'Leads arrive three ways. An Arive file in App Intake, Qualification or Pre-Approved shows up on **Leads** on its own, re-synced every few minutes. **New lead** adds someone by hand. And a homebuyer who taps **Get Pre-Approved** in Blueprint lands on your Leads with their numbers already attached.',
    'Blueprint leads show as **BP Lead** until you open the Arive file with the same email, then the Arive row takes over and keeps the Blueprint link. Last email in and out come from your Gmail, so you can see who has gone quiet.',
  ]),
  dict(id='build', title='Build their Blueprint', body=[
    'Open the lead and click **Open in Blueprint**, or start in Blueprint with **Import from Arive**. Your name, phone and NMLS fill in from your profile.',
    'Build two or three options (FHA against Conventional, a buy-down against none) so **Compare** has something to show. Any option can be hidden from the borrower or made view-only, and **Preview as borrower** shows exactly what they will see.',
  ]),
  dict(id='send', title='Send it', body=[
    'Send it from your own Gmail as "Your personalized mortgage Blueprint" with an **Open my Blueprint** button, or copy the link into a thread you already have going.',
    'The link is private. Your borrower signs in with Google or a one-time code we email them, using the email you have on file. Anyone else who gets the link sees "This blueprint is private."',
  ]),
  dict(id='access', title='Control who sees it', body=[
    '**Manage access** on the lead sets what they can do (view only, adjust, or full edit), sets an expiry date, and makes a new link if one went to the wrong person. **People with access** lists every email the link opens for; add a spouse, parent or agent, or remove anyone.',
    'Once you have checked their documents, lock **Income**, **Debts**, **Assets** or **Credit Score**. They see "Income verified by your loan officer" and the section stays put.',
  ]),
  dict(id='engage', title="See what they're doing", img='ops-dashboard.webp', alt='Ops Dashboard with Blueprint Activity', caption='The Dashboard. Blueprint Activity runs down the right side.', body=[
    'Manage access shows when they first signed in and last opened it. **Blueprint Activity** on your Dashboard lists every open and every change, and **Changes** shows exactly what moved: price, rate, down payment.',
    'On a call together? You both see a **Live** bar in Blueprint, with an outline on the field the other person is touching. **Follow** lets you ride along.',
  ]),
  dict(id='flows', title='Follow up on autopilot', img='ops-crm.webp', alt='Ops CRM email flows', caption='CRM email flows with merge tags and a review queue.', body=[
    'Email flows enroll Arive files automatically when they change stage: Application Sent, Application Received, Pre-Qualified, Pre-Approved. Set them to Review and every email waits for your OK; the Dashboard shows what is going out in the next 48 hours.',
    'Blueprint leads can be added to any flow in two clicks.',
  ]),
  dict(id='live', title='Application to clear to close', img='ops-live.webp', alt='Ops Live Loans', caption='Live Loans: every file from Setup to Closing, with the trackers that matter.', body=[
    'The file moves from Leads into **Live Loans**: Setup, Disclosed, UW, CTC, Closing, synced from Arive. Appraisal, title, insurance, lock and CD trackers show what is stuck without opening Arive.',
    '**Send Timeline Email** updates the borrower, both agents and escrow in one click, from your Gmail.',
  ]),
  dict(id='after', title='After closing', img='ops-refi.webp', alt='Ops Refi Hunter', caption='Refi Hunter flags past clients when today\'s rates would save them money.', body=[
    'The **Closed** checklist keeps post-close follow-through from slipping: the funding email, calls to clients and agents, the six-month check-in, comp and the review request.',
    '**Refi Hunter** watches every past client\'s rate and flags them, with the monthly savings, when the market crosses their strike price.',
  ]),
  dict(id='start', title='Getting started', step=False, body=[
    'About 15 minutes, once: sign in with Google, check your profile, paste three keys from Arive, connect Gmail, send your first Blueprint. A checklist in the app ticks each step off as you go.',
    'A **Test book** with a full, made-up pipeline lets you try everything (and record demos) without touching a real client.',
  ]),
]

# ── For borrowers (mirrors Ops Help Center "Borrower guide") ────────────────
BR_STEPS = [
  dict(id='open', title='Open your Blueprint', img='bp-signin.webp', phone=True, alt='Blueprint sign-in screen', caption='The sign-in screen your loan officer\'s link opens.', body=[
    'Tap the link your loan officer sent. Choose **Continue with Google**, or **Sign in with email** and then **Email me a code**.',
    'If you used email, look for "Your RealStack Blueprint sign-in code" and type the code in. It works once and lasts 60 minutes. The email has no sign-in link on purpose; just type the code.',
    'Use the email your loan officer has for you. The link only opens for the people on your file, which is what keeps your numbers private. You sign in once per device.',
  ]),
  dict(id='stuck', title='If something goes wrong', body=[
    '**"This blueprint is private"**: you signed in with a different email. Tap Use a different email, or ask your loan officer to add the one you used.',
    '**"Almost ready"**: your loan officer is still building your numbers. Tap Check again later.',
    '**"Link Not Found"**: the link is old. Use the Email, Call or Schedule buttons on that screen to get a fresh one.',
    '**No code?** Check spam and promotions, or use Continue with Google.',
  ]),
  dict(id='phone', title='Put it on your phone', body=[
    '**iPhone:** get Mortgage Blueprint from the App Store, or open your link in Safari, tap Share, then Add to Home Screen.',
    '**Android:** open your link in Chrome, tap the menu, then Install app.',
  ]),
  dict(id='numbers', title='Change the numbers', body=[
    'Tap any number to change it. Try the price, your down payment (watch mortgage insurance change at 20%), the rate and the property taxes. **Monthly Payment**, **Cash to Close** and **Pre-Qualified?** update instantly.',
    'A section marked "verified by your loan officer" has been checked against your documents and is locked. A view-only option is a fixed quote; tap Duplicate to try your own version. Made a mistake? **Version history** puts it back.',
  ]),
  dict(id='compare', title='Compare and share', body=[
    '**Compare** puts your options side by side. On the **Share** tab, Email Me This Worksheet sends you a PDF (your loan officer gets a copy), and Save Scenario as PDF downloads it.',
    'To add a spouse, co-borrower or agent, go to **Team**, then People with access, and add their email. They sign in with that email.',
  ]),
  dict(id='together', title='Work on it together', body=[
    'Your changes save automatically and your loan officer sees them. On a call, you will both see a Live bar with each other\'s name, so they can follow along as you go.',
  ]),
  dict(id='next', title='Ready to move forward', body=[
    'Tap **Get Pre-Approved Now** on the Share tab (or More on a phone). Your loan officer gets your request with the scenario you were looking at and will reach out with next steps.',
  ]),
  dict(id='privacy', title='Your account and privacy', body=[
    'Only you, the people on your list and your loan officer\'s team can open your Blueprint, even with the link. **Settings, Your account** shows the email you are signed in with and has Sign out, plus Export or delete my account.',
    'Blueprint gives estimates, not a loan offer. Your official numbers come on your Loan Estimate. You must be 18 or older to use it.',
  ]),
]

# ── How it works (two lanes) ────────────────────────────────────────────────
STAGES = [
  ('The lead arrives', 'Arive files, a quick New lead, or a homebuyer\'s Get Pre-Approved request all land on your Leads tab, with Gmail history attached.', 'Finds you through a referral, or plays with the free Blueprint calculator and taps Get Pre-Approved.'),
  ('You build the Blueprint', 'Import the file from Arive and build two or three real options in minutes. Your name, phone and NMLS fill in.', 'Nothing to do yet. Their Blueprint is being built with their real numbers, ready the moment they open it.'),
  ('You send it', 'One email from your own Gmail with an Open my Blueprint button, or a link you paste anywhere.', 'Gets "Your personalized mortgage Blueprint" and taps the button.'),
  ('They sign in', 'Manage access shows the moment they first sign in. You decide who else can open it and what they can change.', 'Signs in with Google or a one-time code. Only the emails on their file can open it.'),
  ('You work it together', 'Blueprint Activity shows every change. Lock income and assets once you have checked the documents.', 'Changes price, down payment and rate, compares options, and adds a spouse or agent.'),
  ('Application to close', 'The file moves to Live Loans. Timeline emails and stage-based follow-ups go out from your Gmail.', 'Gets clear updates at every milestone, from the same loan officer they have been talking to.'),
  ('After closing', 'The closing checklist, then Refi Hunter flags them when rates would save them money.', 'Keeps their Blueprint, and hears from you when a refinance actually makes sense.'),
]

def flow_body():
    rows = []
    for i, (name, lo, br) in enumerate(STAGES, 1):
        lo_cell = f'<div class="cell lo"><p class="who">You, in Ops</p><p>{md(lo)}</p></div>'
        br_cell = (f'<div class="cell borrower"><p class="who">Your borrower, in Blueprint</p><p>{md(br)}</p></div>'
                   if br else '<div class="cell borrower empty" aria-hidden="true"></div>')
        rows.append(f'        <div class="stage"><div class="stage-name"><span class="num">STAGE {i:02d}</span><h3>{html.escape(name)}</h3></div>{lo_cell}{br_cell}</div>')
    return f"""      <div class="hero">
        <p class="overline">How RealStack works</p>
        <h1>From first call to funded loan, on one platform.</h1>
        <p class="sub">You run the deal in <strong>RealStack Ops</strong>. Your borrower plans in <strong>Mortgage Blueprint</strong>. Here is what each of you sees at every step.</p>
      </div>
      <div class="flow">
        <div class="lane-head"><span></span><span>You, in Ops</span><span>Your borrower, in Blueprint</span></div>
{chr(10).join(rows)}
      </div>
      <div class="block center">
        <p class="overline">See it in action</p>
        <h2 style="margin-top:8px">Blueprint and Ops in 43 seconds</h2>
        <div class="player" data-film style="margin-top:20px">
          <video src="/demo/together/wide.mp4" poster="/demo/together/poster.jpg"
            data-wide="/demo/together/wide.mp4" data-wide-poster="/demo/together/poster.jpg"
            data-tall="/demo/together/tall.mp4" data-tall-poster="/demo/together/poster-tall.jpg"
            controls muted playsinline preload="metadata" aria-label="RealStack product film"></video>
        </div>
      </div>
      <div class="block">
        <div class="center"><p class="overline">The guides</p><h2 style="margin-top:8px">Step by step, with screens.</h2></div>
        <div class="cards">
          <a class="card" href="/guides/loan-officer"><h3>For loan officers</h3><p>One file end to end in Ops: leads, sending a Blueprint, controlling access, follow-up, live loans and after closing.</p><span class="go">Read the guide</span></a>
          <a class="card" href="/guides/borrower"><h3>For borrowers</h3><p>The page you send your clients: how to open their Blueprint, change the numbers, share it and get pre-approved.</p><span class="go">Read the guide</span></a>
        </div>
      </div>
      <div class="ctas">
        <a class="btn btn-primary" href="/#pricing">See pricing</a>
        <a class="btn btn-secondary" href="{CAL}" target="_blank" rel="noopener noreferrer">Book a demo</a>
        <a class="btn btn-secondary" href="/demo/ops">Watch the Ops demo</a>
      </div>"""

PAGES = {
  '': page('', 'How RealStack Works',
           'From first call to funded loan: what the loan officer sees in RealStack Ops and what the borrower sees in Mortgage Blueprint, step by step.',
           flow_body(), film=True),
  'loan-officer': page('loan-officer', 'RealStack Guide for Loan Officers',
           'One loan file end to end in RealStack Ops: leads, sending a Mortgage Blueprint, access control, follow-up, live loans and after closing.',
           guide_body('Guide for loan officers', 'One file, start to finish.',
                      'How a lead becomes a funded loan in **RealStack Ops**, with your borrower working their numbers in **Mortgage Blueprint** alongside you.',
                      LO_STEPS, [('See pricing', '/#pricing', True), ('Book a demo', CAL, False), ('Watch the Ops demo', '/demo/ops', False)])),
  'borrower': page('borrower', 'Mortgage Blueprint Borrower Guide',
           'How to open the Mortgage Blueprint your loan officer shared, change the numbers, compare options, add people and get pre-approved.',
           guide_body('Mortgage Blueprint · borrower guide', 'Your Blueprint, step by step.',
                      'Your loan officer built you a **Mortgage Blueprint**: a private, live view of your home loan options. Change the numbers, compare options and see exactly what you would pay.',
                      BR_STEPS, [('Open Blueprint', BP, True), ('Get the iPhone app', APP_STORE, False)], numbered=False)),
}

for slug, content in PAGES.items():
    d = os.path.join(ROOT, 'public', 'guides', slug) if slug else os.path.join(ROOT, 'public', 'guides')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w') as f:
        f.write(content)
    print('wrote', os.path.join(d, 'index.html'))
