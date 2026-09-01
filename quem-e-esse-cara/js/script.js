// =========================================================
// QUEM É ESSE CARA? — interatividade
// =========================================================

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- 1. Sequência de abertura (typewriter) ---------- */
  const lines = [
    { el: document.querySelector('.line-1'), text: 'ENTÃO... VOCÊ QUER SABER QUEM É O GUILHERME?', pause: 900 },
    { el: document.querySelector('.line-2'), text: 'Justo.', pause: 700 },
    { el: document.querySelector('.line-3'), text: 'Prepare-se para informações que provavelmente poderiam ter sido descobertas durante uma conversa normal.', pause: 400 },
  ];
  const btnConhecer = document.getElementById('btnConhecer');
  const aberturaPhoto = document.querySelector('.abertura-photo');

  function typeLine(line, speed = 28) {
    return new Promise(resolve => {
      if (!line.el) return resolve();
      line.el.classList.add('typing');
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
    for (const line of lines) {
      await typeLine(line);
    }
    if (aberturaPhoto) aberturaPhoto.classList.add('show');
    if (btnConhecer) {
      btnConhecer.classList.add('is-ready');
      btnConhecer.removeAttribute('tabindex');
    }
  }
  runOpening();

  if (btnConhecer) {
    btnConhecer.addEventListener('click', () => {
      document.getElementById('sonic').scrollIntoView({ behavior: 'smooth' });
    });
  }

  /* ---------- 2. Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
      }
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
      const scored = Math.random() < 0.22; // café com leite não acerta muito
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

});
