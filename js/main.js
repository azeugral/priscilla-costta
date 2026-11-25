(() => {
  const WA = '559870151421';

  // menu do celular
  const bt = document.querySelector('.menu-bt'), menu = document.getElementById('menu');
  bt.addEventListener('click', () => {
    const ab = bt.getAttribute('aria-expanded') === 'true';
    bt.setAttribute('aria-expanded', String(!ab)); menu.hidden = ab;
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.hidden = true; bt.setAttribute('aria-expanded', 'false'); }));

  // entrada ao rolar (subida leve)
  const alvos = document.querySelectorAll('.cab, .area, .passos li, .sobre-foto, .sobre-txt, .galeria figure, .marcos li, .escritorio > *, .faq, .form, .nota');
  alvos.forEach(el => el.classList.add('rv'));
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  alvos.forEach(el => io.observe(el));

  // contrato: grifos aparecem quando a folha entra na tela
  const folha = document.querySelector('.folha');
  new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { folha.classList.add('vis'); o.disconnect(); } }), { threshold: .35 }).observe(folha);
  document.querySelectorAll('.nota').forEach(n => {
    const m = folha.querySelector(`mark[data-n="${n.dataset.n}"]`);
    n.addEventListener('mouseenter', () => { m.classList.add('foco'); n.classList.add('foco'); });
    n.addEventListener('mouseleave', () => { m.classList.remove('foco'); n.classList.remove('foco'); });
  });
  folha.querySelectorAll('mark').forEach(m => {
    const n = document.querySelector(`.nota[data-n="${m.dataset.n}"]`);
    m.addEventListener('mouseenter', () => { m.classList.add('foco'); n.classList.add('foco'); });
    m.addEventListener('mouseleave', () => { m.classList.remove('foco'); n.classList.remove('foco'); });
  });

  // formulário: monta a mensagem e abre o WhatsApp
  const f = document.getElementById('form');
  f.addEventListener('submit', ev => {
    ev.preventDefault();
    const d = new FormData(f), nome = (d.get('nome') || '').trim(), erro = f.querySelector('.erro');
    if (!nome) { erro.hidden = false; f.nome.focus(); return; }
    erro.hidden = true;
    const l = [`Olá, Dra. Priscilla! Sou *${nome}* e gostaria de uma análise do meu caso.`, ''];
    l.push(`*Perfil:* ${d.get('perfil')}`);
    l.push(`*Assunto:* ${d.get('assunto')}`);
    const cid = (d.get('cidade') || '').trim(); if (cid) l.push(`*Cidade:* ${cid}`);
    const bco = (d.get('banco') || '').trim(); if (bco) l.push(`*Banco/instituição:* ${bco}`);
    const rel = (d.get('relato') || '').trim(); if (rel) l.push(`*Relato:* ${rel}`);
    l.push(`*Melhor horário:* ${d.get('horario')}`);
    l.push('', '(mensagem enviada pelo site)');
    window.open(`https://wa.me/${WA}?text=${encodeURIComponent(l.join('\n'))}`, '_blank', 'noopener');
  });
  f.nome.addEventListener('input', () => { if (f.nome.value.trim()) f.querySelector('.erro').hidden = true; });
})();
