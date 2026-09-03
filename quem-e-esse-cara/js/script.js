// =========================================================
// QUEM É ESSE CARA? v2 — interatividade
// =========================================================

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- 0. Gate / triagem ---------- */
  const btnSingle = document.getElementById('btnSingle');
  const btnTaken = document.getElementById('btnTaken');
  const gateSection = document.getElementById('gate');

  if (btnSingle) {
    btnSingle.addEventListener('click', () => {
      gateSection.style.display = 'none';
      runOpening();
      document.getElementById('abertura').scrollIntoView({ behavior: 'instant' in window ? 'instant' : 'auto' });
    });
  }

  if (btnTaken) {
    btnTaken.addEventListener('click', () => {
      document.body.classList.add('is-blocked');
      window.scrollTo(0, 0);
    });
  }

  /* ---------- 1. Sequência de abertura (typewriter) ---------- */
  const lines = [
    { el: document.querySelector('.line-1'), text: 'Então você quer saber quem é o Guilherme?', pause: 900 },
    { el: document.querySelector('.line-2'), text: 'Excelente decisão.', pause: 650 },
    { el: document.querySelector('.line-3'), text: 'Ou uma decisão questionável.', pause: 500 },
    { el: document.querySelector('.line-4'), text: 'Mas agora já estamos aqui.', pause: 300 },
  ];
  const btnConhecer = document.getElementById('btnConhecer');
  const aberturaPhoto = document.querySelector('.abertura-photo');
  let openingStarted = false;

  function typeLine(line, speed = 26) {
    return new Promise(resolve => {
      if (!line.el) return resolve();
      let i = 0;
      const interval = setInterval(() => {
        line.el.textContent = line.text.slice(0, i + 1);
        i++;
        if (i >= line.text.length) {
          clearInterval(interval);
          setTimeout(resolve, line.pause);
        }
      }, speed);
    });
  }

  async function runOpening() {
    if (openingStarted) return;
    openingStarted = true;
    for (const line of lines) {
      await typeLine(line);
    }
    if (aberturaPhoto) aberturaPhoto.classList.add('show');
    if (btnConhecer) {
      btnConhecer.classList.add('is-ready');
      btnConhecer.removeAttribute('tabindex');
    }
  }

  if (btnConhecer) {
    btnConhecer.addEventListener('click', () => {
      document.getElementById('sonic').scrollIntoView({ behavior: 'smooth' });
    });
  }

  /* ---------- 2. Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
    });
  }, { threshold: 0.2 });
  revealEls.forEach(el => revealObserver.observe(el));

  /* ---------- 3. Nav ativa por seção ---------- */
  const navLinks = document.querySelectorAll('.world-nav a');
  const sections = document.querySelectorAll('.world');
  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  }, { threshold: 0.5 });
  sections.forEach(sec => navObserver.observe(sec));

  /* ---------- 4. Arremesso de basquete ---------- */
  const shootBtn = document.getElementById('shootBtn');
  const shootResult = document.getElementById('shootResult');
  const misses = [
    'Errou feio. Mas com estilo.',
    'Bateu na tabela, no aro e no orgulho.',
    'Quase. "Quase" não conta ponto.',
    'Air ball. Clássico.',
    'A bola nem quis saber.',
  ];
  const hits = [
    'CESTA! Ninguém esperava, inclusive ele.',
    'ENTROU! Guarda essa gravação.',
    'Milagre confirmado: pontuou.',
  ];
  if (shootBtn) {
    shootBtn.addEventListener('click', () => {
      const scored = Math.random() < 0.22;
      const pool = scored ? hits : misses;
      shootResult.textContent = pool[Math.floor(Math.random() * pool.length)];
      shootBtn.classList.remove('shake');
      void shootBtn.offsetWidth;
      shootBtn.classList.add('shake');
    });
  }

  /* ---------- 5. Barras de status (cyber) ---------- */
  const statusRows = document.querySelectorAll('.status-row');
  const statusObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const row = entry.target;
        const value = row.getAttribute('data-value');
        row.querySelector('.bar i').style.setProperty('--fill', value + '%');
        row.classList.add('filled');
        statusObserver.unobserve(row);
      }
    });
  }, { threshold: 0.4 });
  statusRows.forEach(row => statusObserver.observe(row));

  /* ---------- 6. Hit counter (contador 90's, cosmético) ---------- */
  const hitCounter = document.getElementById('hitCounter');
  if (hitCounter) {
    const base = 130482 + Math.floor(Math.random() * 40);
    hitCounter.textContent = String(base).padStart(6, '0');
  }

});
