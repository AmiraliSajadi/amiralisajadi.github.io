const topicNames = {risks: 'Understanding security risks', analysis: 'Improving static vulnerability analysis', exploitation: 'Exploitation and red teaming', human: 'Human aspects of software engineering'};
const papersNode = document.getElementById('papers');
const filterButtons = [...document.querySelectorAll('[data-filter]')];

function filterPapers(topic) {
  let visible = 0;
  document.querySelectorAll('.paper').forEach(paper => {
    paper.hidden = topic !== 'all' && paper.dataset.topic !== topic;
    if (!paper.hidden) visible++;
  });
  filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === topic)));
  document.getElementById('count').textContent = visible + (visible === 1 ? ' project' : ' projects');
  const url = new URL(location.href);
  if (topic === 'all') url.searchParams.delete('topic');
  else url.searchParams.set('topic', topic);
  history.replaceState(null, '', url);
}
if (papersNode) {
  const requestedTopic = new URLSearchParams(location.search).get('topic');
  filterPapers(Object.hasOwn(topicNames, requestedTopic) ? requestedTopic : 'all');
  filterButtons.forEach(button => button.addEventListener('click', () => filterPapers(button.dataset.filter)));
  addEventListener('popstate', () => {
    const topic = new URLSearchParams(location.search).get('topic');
    filterPapers(Object.hasOwn(topicNames, topic) ? topic : 'all');
  });
}

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}
const imageButtons = [...document.querySelectorAll('[data-figure-key]')];
if (imageButtons.length) {
  const dialog = make('dialog', 'figure-dialog');
  const closeButton = make('button', 'dialog-close', 'Close ×');
  closeButton.type = 'button';
  const title = make('h2');
  title.id = 'figure-title';
  const image = make('img');
  const caption = make('p');
  dialog.setAttribute('aria-labelledby', title.id);
  dialog.append(closeButton, title, image, caption);
  document.body.append(dialog);
  closeButton.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  let paperData;
  function loadPapers() {
    if (!paperData) paperData = fetch('/research.json').then(response => {
      if (!response.ok) throw new Error('Research data unavailable');
      return response.json();
    }).catch(error => {paperData = undefined; throw error;});
    return paperData;
  }
  imageButtons.forEach(button => button.addEventListener('click', async () => {
    try {
      const papers = await loadPapers();
      const paper = papers.find(item => item.id === button.dataset.figureKey);
      if (!paper) return;
      title.textContent = paper.title;
      image.src = '/assets/' + paper.image;
      image.alt = paper.imageAlt || 'Figure from ' + paper.title;
      caption.textContent = [paper.imageCaption, paper.venue, paper.year].filter(Boolean).join(' · ');
      dialog.showModal();
    } catch {
      const source = button.querySelector('img');
      title.textContent = source.alt;
      image.src = source.src;
      image.alt = source.alt;
      caption.textContent = '';
      dialog.showModal();
    }
  }));
}


const journeyArt = document.querySelector('.journey-art');
if (journeyArt) {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const journeyControl = document.querySelector('.journey-control');
  if (journeyControl) journeyControl.addEventListener('click', () => {
    const paused = journeyArt.classList.toggle('is-paused');
    const label = paused ? 'Resume animation' : 'Pause animation';
    journeyControl.dataset.paused = String(paused);
    journeyControl.setAttribute('aria-label', label);
    journeyControl.title = label;
  });
  const startJourney = () => {
    if (!reducedMotion.matches) {
      journeyArt.classList.add('is-active');
      if (journeyControl) journeyControl.hidden = false;
    }
  };
  if ('IntersectionObserver' in window) {
    const journeyObserver = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        startJourney();
        journeyObserver.disconnect();
      }
    }, {threshold: 0.25});
    journeyObserver.observe(journeyArt);
  } else {
    startJourney();
  }
}

// Follow the device initially, then remember an explicit choice across pages.
const themeToggle = document.querySelector('.theme-toggle');
const systemTheme = matchMedia('(prefers-color-scheme: dark)');
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  if (themeToggle) {
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeToggle.setAttribute('aria-pressed', String(theme === 'dark'));
    themeToggle.innerHTML = `<i data-lucide="${theme === 'dark' ? 'sun' : 'moon'}" aria-hidden="true"></i>`;
  }
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#111923' : '#f5f8fc');
  if (typeof lucide !== 'undefined') lucide.createIcons();
}
let savedTheme;
try { savedTheme = localStorage.getItem('amirali-theme'); } catch (_) {}
applyTheme(['light','dark'].includes(savedTheme) ? savedTheme : systemTheme.matches ? 'dark' : 'light');
if (themeToggle) themeToggle.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(theme);
  try { localStorage.setItem('amirali-theme', theme); } catch (_) {}
});
systemTheme.addEventListener('change', event => {
  let chosen;
  try { chosen = localStorage.getItem('amirali-theme'); } catch (_) {}
  if (!chosen) applyTheme(event.matches ? 'dark' : 'light');
});
