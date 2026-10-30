"""Render the static site pages from the research data and page templates."""

from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
PAPERS = json.loads((ROOT / 'research.json').read_text())
BY_ID = {p['id']: p for p in PAPERS}
SPACED_FIGURES = {'llm', 'emotions'}

TOPICS = [
    ('exploitation', 'Exploitation and red teaming', 'Exploitability confirmation, agent trajectory analysis, and planned exploit-based red teaming.', ['axe', 'report', 'trace']),
    ('analysis', 'Improving static vulnerability analysis', 'CodeQL false positives, query refinements, agent adaptation, and developer feedback.', ['sast']),
    ('risks', 'Understanding security risks', 'Security awareness in programming assistance and vulnerabilities introduced by AI-generated patches.', ['repair', 'llm']),
    ('human', 'Human aspects of software engineering', 'Trust, emotions, and psycholinguistic analysis in developer communication.', ['trust', 'emotions', 'psych']),
]
SHORT = {'repair': 'How safe are AI-generated patches?', 'trace': 'TraceView', 'llm': 'Do LLMs consider security?', 'axe': 'AXE', 'sast': 'CodeQL false positives and query refinements', 'report': 'Vulnerability reports and AI agents', 'trust': 'Interpersonal trust in OSS', 'emotions': 'Emotions in developer conversations', 'psych': 'Psycholinguistic analysis in SE'}
VENUES = {'repair': 'TOSEM', 'trace': 'ICSME', 'llm': 'EMSE', 'axe': 'Under review', 'sast': 'Preprint', 'report': 'Ongoing', 'trust': 'ICSE NIER', 'emotions': 'ESEC/FSE IVR', 'psych': 'IST'}

def shell(title, active, main):
    """Wrap page content in the shared navigation and site layout."""
    nav = ''.join(f'<a href="{href}"'+(' aria-current="page"' if key == active else '')+f'>{label}</a>' for key, href, label in [('research','/research/','Research'),('about','/about/','About'),('contact','/contact/','Contact')])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Amirali Sajadi. Research on AI-assisted software development, software security, and vulnerability analysis at Drexel University."><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#f5f8fc"><script>try{{const t=localStorage.getItem("amirali-theme");document.documentElement.dataset.theme=t|| (matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light")}}catch(e){{}}</script><title>{title}</title><link rel="stylesheet" href="/style.css"><script src="/vendor/lucide.min.js" defer></script><script src="/script.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><a class="home-link" href="/">Amirali Sajadi</a><nav aria-label="Main navigation">{nav}</nav><button class="theme-toggle" type="button" aria-label="Switch to dark mode"><i data-lucide="moon" aria-hidden="true"></i></button></header>{main}<footer class="wrap"><span>Amirali Sajadi</span><div><a href="/assets/cv.pdf" target="_blank" rel="noopener">CV</a><a href="https://scholar.google.com/citations?user=wyZsULIAAAAJ&hl=en" target="_blank" rel="noopener">Scholar</a><a href="https://github.com/AmiraliSajadi" target="_blank" rel="noopener">GitHub</a><a href="mailto:amirali.sajadi@drexel.edu">Email</a></div></footer></body></html>'''

def tile(key):
    """Render a research tile for the home page."""
    p = BY_ID[key]
    figure_class = '' if key in SPACED_FIGURES else ' figure-fill'
    return f'''<article class="work-tile"><button class="tile-image{figure_class}" type="button" data-figure-key="{key}" aria-label="Enlarge image for {escape(p['title'],quote=True)}"><img src="/assets/{p['image']}" alt="{escape(p.get('imageAlt', 'Figure from ' + p['title']),quote=True)}" loading="lazy"></button><div class="tile-meta">{VENUES[key]} <span>{p['year']}</span></div><h3><a href="/research/#paper-{key}">{SHORT[key]}</a></h3><p>{escape(p['summary'])}</p></article>'''

intro = '''<section class="profile-intro" aria-labelledby="profile-name"><aside class="home-profile"><a class="home-profile-photo" href="/about/" aria-label="About Amirali Sajadi"><img src="/assets/portrait.jpg" width="1388" height="1328" alt="Amirali Sajadi"></a><h1 id="profile-name">Amirali Sajadi</h1><p class="profile-affiliation">PhD Candidate<br>Computer Science<br>Drexel University</p><a class="profile-about-link" href="/about/">About me ↗</a></aside><div class="home-overview"><div class="intro-label">Computer science · Drexel University</div><h2>Software security and AI</h2><p>I study security risks in AI-generated code and develop methods for vulnerability analysis and exploitability confirmation.</p><p class="intro-secondary">My earlier work examined interpersonal trust and emotions in developer conversations, and the use of psycholinguistic tools in software engineering.</p><div class="overview-links"><a class="primary-link" href="/research/">Explore my research <i data-lucide="arrow-up-right" aria-hidden="true"></i></a><a href="/assets/cv.pdf" target="_blank" rel="noopener">CV ↗</a><a href="https://scholar.google.com/citations?user=wyZsULIAAAAJ&hl=en" target="_blank" rel="noopener">Google Scholar ↗</a></div></div></section>'''
themes = ''
for n, (key, title, summary, ids) in enumerate(TOPICS, 1):
    themes += f'''<section class="research-theme theme-{key}" aria-labelledby="theme-{key}"><div class="theme-heading"><div class="theme-topline"><span class="theme-icon"><i data-lucide="{dict(exploitation='bug',analysis='scan-line',risks='shield-check',human='messages-square')[key]}" aria-hidden="true"></i></span><span class="theme-index">{'Earlier work' if key == 'human' else f'Research theme 0{n}'}</span></div><h2 id="theme-{key}">{title}</h2><p>{summary}</p><a class="theme-link" href="/research/?topic={key}">Papers and details <span aria-hidden="true">↗</span></a></div><div class="work-grid grid-count-{len(ids)}">{''.join(tile(i) for i in ids)}</div></section>'''
(ROOT / 'index.html').write_text(shell('Amirali Sajadi', 'home', f'<main id="main" class="wrap home-main">{intro}{themes}</main>'))

def paper_row(p):
    """Render one publication entry for the research page."""
    figure_class = '' if p['id'] in SPACED_FIGURES else ' figure-fill'
    meta_class = ' paper-meta-with-track' if p.get('track') else ''
    track = f'<span class="paper-track">{escape(p["track"])}</span>' if p.get('track') else ''
    pdf = f'/assets/papers/{p["pdf"]}' if p.get('pdf') else None
    heading = f'<a href="{pdf}" target="_blank" rel="noopener">{escape(p["title"])}</a>' if pdf else escape(p['title'])
    links = ''
    for key, label in [('pdf','Paper'),('code','Code'),('demo','Video')]:
        if p.get(key):
            url = pdf if key == 'pdf' else p[key]
            links += f'<a href="{url}" target="_blank" rel="noopener">{label} ↗</a>'
    abstract = ''
    if p.get('abstract') and p['abstract'] != p['summary']:
        abstract = f'<details><summary>Abstract</summary><p>{escape(p["abstract"])}</p></details>'
    authors = escape(p['authors']).replace('Amirali Sajadi', '<strong>Amirali Sajadi</strong>')
    return f'''<article class="paper" id="paper-{p['id']}" data-topic="{p['topic']}"><button class="paper-figure{figure_class}" type="button" data-figure-key="{p['id']}" aria-label="Enlarge image for {escape(p['title'],quote=True)}"><img src="/assets/{p['image']}" alt="{escape(p.get('imageAlt', 'Figure from ' + p['title']),quote=True)}" loading="lazy"></button><div><div class="paper-meta{meta_class}"><span class="paper-venue">{escape(p['venue'])}</span>{track}<span class="paper-year">{p['year']}</span></div><h2>{heading}</h2><p class="paper-summary">{escape(p['summary'])}</p><p class="authors">{authors}</p><div class="paper-actions">{links}</div>{abstract}</div></article>'''
filters = ''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{label}</button>' for key, label in [('all','All work'),('exploitation','Exploitation'),('analysis','Static analysis'),('risks','Security risks'),('human','Human aspects')])
research = f'''<main id="main" class="wrap page-main"><div class="page-intro"><h1>Research</h1><p>Published papers, preprints, and ongoing work.</p></div><div class="research-toolbar"><div class="filters" role="group" aria-label="Filter research by topic">{filters}</div><span id="count" class="research-count" aria-live="polite">9 projects</span></div><div id="papers">{''.join(paper_row(p) for p in PAPERS)}</div></main>'''
(ROOT / 'research/index.html').write_text(shell('Research · Amirali Sajadi', 'research', research))
about = '''<main id="main" class="wrap page-main">
<div class="page-intro"><h1>About</h1></div>
<div class="about-layout">
  <figure class="about-photo"><img src="/assets/personal/about-portrait.png" alt="Amirali outdoors at dusk with city lights in the background" width="886" height="1329"></figure>
  <div class="about-copy">
    <p>I’m a computer science PhD candidate at Drexel University, where I’ve been since 2022. I work with <a href="https://preethac.github.io/" target="_blank" rel="noopener">Dr. Chatterjee</a> on software security and AI.</p>
    <p>I study how AI coding agents affect software security. My goal is to reduce the risks they introduce and use their capabilities to find and confirm vulnerabilities.</p>
    <p>My earlier work studied trust and emotions in developer conversations.</p>
    <p>I also teach computer science classes, assist with other courses, and mentor undergraduate researchers.</p>
    <div class="about-links"><a href="/assets/cv.pdf" target="_blank" rel="noopener">Curriculum vitae ↗</a><a href="/contact/">Contact ↗</a></div>
  </div>
</div>
<section class="about-gallery" aria-labelledby="outside-research"><h2 id="outside-research">Outside research</h2>
  <figure class="photo-hike"><img src="/assets/personal/hike.png" alt="Amirali beside a wooded creek with a companion" width="1273" height="849" loading="lazy"><figcaption>I like getting out into nature whenever I can, even if it’s just for a short hike.</figcaption></figure>
  <figure class="photo-work"><img src="/assets/personal/working-at-home.png" alt="Amirali sitting at his desk with a monitor and notebook at home" width="739" height="946" loading="lazy"><figcaption>Working from home</figcaption></figure>
  <figure class="photo-climb"><img src="/assets/personal/climbing.png" alt="Amirali climbing an indoor bouldering wall" width="747" height="702" loading="lazy"><figcaption>Climbing</figcaption></figure>
  <figure class="photo-watch"><img src="/assets/personal/watches.png" alt="Amirali showing a watch on his wrist" width="996" height="1329" loading="lazy"><figcaption>I collect watches!</figcaption></figure>
  <figure class="photo-trail"><img src="/assets/personal/trail-hike.png" alt="Amirali and a companion posing on a wooded trail" width="1772" height="1329" loading="lazy"><figcaption>Out on the trails</figcaption></figure>
  <figure class="photo-yellowstone"><img src="/assets/personal/yellowstone.png" alt="Amirali at Yellowstone, with geothermal steam and two companions in the background" width="1772" height="1329" loading="lazy"><figcaption>Yellowstone :)</figcaption></figure>
</section>
</main>'''

(ROOT / 'about/index.html').write_text(shell('About · Amirali Sajadi', 'about', about))
journey_svg = (ROOT / 'assets/tehran-philadelphia.svg').read_text()
contact = f'''<main id="main" class="wrap page-main contact-page"><div class="contact-layout"><div class="page-intro"><h1>Contact</h1></div><div class="contact-copy"><p class="contact-email"><a href="mailto:amirali.sajadi@drexel.edu">amirali.sajadi@drexel.edu ↗</a></p><div class="contact-grid"><section><h2>At Drexel</h2><p>College of Computing and Informatics<br>Drexel University<br>Philadelphia, Pennsylvania</p></section><section><h2>Elsewhere</h2><div class="contact-links"><a href="https://scholar.google.com/citations?user=wyZsULIAAAAJ&hl=en" target="_blank" rel="noopener">Google Scholar ↗</a><a href="https://github.com/AmiraliSajadi" target="_blank" rel="noopener">GitHub ↗</a><a href="https://www.linkedin.com/in/amirali-sajadi-a169a821b/" target="_blank" rel="noopener">LinkedIn ↗</a><a href="/assets/cv.pdf" target="_blank" rel="noopener">Curriculum vitae ↗</a></div></section></div></div><figure class="contact-visual">{journey_svg}<button class="journey-control" type="button" aria-label="Pause animation" title="Pause animation" data-paused="false" hidden></button></figure></div></main>'''
(ROOT / 'contact/index.html').write_text(shell('Contact · Amirali Sajadi', 'contact', contact))
print('Rendered 4 pages')
