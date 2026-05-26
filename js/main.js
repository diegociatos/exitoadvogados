document.querySelectorAll('.menu-toggle').forEach(button => {
  button.addEventListener('click', () => document.querySelector('.nav').classList.toggle('open'));
});

const visualStyle = document.createElement('style');
visualStyle.textContent = `
  html,
  body {
    max-width: 100%;
    overflow-x: hidden;
  }

  .method-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .method-card {
    padding: 24px 28px;
    border-radius: 18px;
  }

  .method-card b {
    display: block;
    font-size: 21px;
    line-height: 1.25;
  }

  .method-card p {
    margin: 10px 0 0;
    text-align: left;
    line-height: 1.55;
    color: #ded7cc;
  }

  .service-grid {
    align-items: stretch;
  }

  @media (min-width: 1101px) {
    .service-grid {
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    }

    .service-grid:has(.service-card:nth-child(5):last-child) {
      grid-template-columns: repeat(5, 1fr);
    }
  }

  .service-card {
    position: relative;
    overflow: hidden;
    min-height: 0;
    padding: 24px;
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    gap: 12px;
    background:
      linear-gradient(145deg, rgba(255,255,255,.98), rgba(252,247,238,.94)),
      radial-gradient(circle at 92% 10%, rgba(227,195,109,.26), transparent 34%);
    border: 1px solid rgba(201,161,74,.32);
    border-radius: 18px;
    box-shadow: 0 16px 38px rgba(35,24,12,.08);
    transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
  }

  .service-card:before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      linear-gradient(90deg, rgba(201,161,74,.9), rgba(227,195,109,.3)) top left / 100% 3px no-repeat,
      linear-gradient(135deg, transparent 0 62%, rgba(201,161,74,.08) 62% 100%);
  }

  .service-card:after {
    content: ">";
    position: absolute;
    right: 18px;
    bottom: 18px;
    width: 28px;
    height: 28px;
    display: grid;
    place-items: center;
    border-radius: 999px;
    color: #17110a;
    background: linear-gradient(135deg, #c9a14a, #e5c36d);
    font-weight: 900;
    opacity: 0;
    transform: translateX(6px);
    transition: .22s ease;
  }

  .service-card:hover {
    transform: translateY(-5px);
    border-color: rgba(201,161,74,.78);
    box-shadow: 0 24px 58px rgba(35,24,12,.14);
  }

  .service-card:hover:after {
    opacity: 1;
    transform: translateX(0);
  }

  .service-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
  }

  .service-icon {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    border-radius: 12px;
    background: #111;
    color: #e3c36d;
    box-shadow: inset 0 0 0 1px rgba(227,195,109,.32), 0 10px 22px rgba(0,0,0,.12);
    font-size: 14px;
    font-style: normal;
    font-weight: 900;
  }

  .service-card span {
    color: #a87925;
    font-size: 12px;
    letter-spacing: .16em;
  }

  .service-card h3 {
    max-width: 100%;
    margin: 2px 0 0;
    font-size: 23px;
    line-height: 1.12;
  }

  .service-desc {
    margin: 0;
    color: #6d6256;
    font-size: 15px;
    line-height: 1.45;
    text-align: left;
  }

  .service-more {
    margin-top: 4px;
    padding-right: 36px;
    color: #8f6720;
    font-size: 13px;
    font-style: normal;
    font-weight: 900;
    letter-spacing: .08em;
    text-transform: uppercase;
  }

  .article-card {
    position: relative;
    overflow: hidden;
    padding: 0;
    display: flex;
    flex-direction: column;
    min-height: 100%;
  }

  .article-cover {
    min-height: 178px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: #fff;
    border-bottom: 1px solid rgba(201,161,74,.38);
    background:
      radial-gradient(circle at 18% 18%, rgba(227,195,109,.32), transparent 28%),
      linear-gradient(135deg, rgba(5,5,5,.96), rgba(34,30,24,.88)),
      var(--cover-image, linear-gradient(135deg, #080808, #211b12));
    background-size: cover;
    background-position: center;
    isolation: isolate;
  }

  .article-cover:before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      linear-gradient(120deg, transparent 0 38%, rgba(227,195,109,.16) 38% 39%, transparent 39% 100%),
      linear-gradient(180deg, rgba(0,0,0,.2), rgba(0,0,0,.72));
    z-index: -1;
  }

  .article-cover-kicker {
    align-self: flex-start;
    border: 1px solid rgba(227,195,109,.55);
    border-radius: 999px;
    padding: 7px 12px;
    color: #f2d98c;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .14em;
    text-transform: uppercase;
    background: rgba(0,0,0,.28);
  }

  .article-cover-title {
    max-width: 92%;
    color: #fff;
    font-size: 24px;
    line-height: 1.08;
    font-weight: 800;
    text-shadow: 0 6px 18px rgba(0,0,0,.45);
  }

  .article-card > .eyebrow,
  .article-card > h3,
  .article-card > p {
    margin-left: 28px;
    margin-right: 28px;
  }

  .article-card > .eyebrow {
    margin-top: 24px;
  }

  .article-card > h3 {
    margin-top: 10px;
  }

  .article-card > p {
    margin-top: 0;
    margin-bottom: 28px;
    text-align: left;
    color: #62594f;
  }

  .article-card[data-cover="patrimonio"] { --cover-image: linear-gradient(135deg, #0b0a08, #5a4420); }
  .article-card[data-cover="financeiro"] { --cover-image: linear-gradient(135deg, #070a0a, #253b32); }
  .article-card[data-cover="previdencia"] { --cover-image: linear-gradient(135deg, #090909, #34314a); }
  .article-card[data-cover="saude"] { --cover-image: linear-gradient(135deg, #080909, #28424a); }
  .article-card[data-cover="indenizacoes"] { --cover-image: linear-gradient(135deg, #090806, #4a2f2f); }

  .blog-index {
    background:
      radial-gradient(circle at 12% 16%, rgba(201,161,74,.12), transparent 28%),
      var(--cream);
  }

  .blog-index .service-hero {
    min-height: 520px;
    padding: 110px 48px 90px;
  }

  .blog-index .service-hero:before {
    background:
      linear-gradient(90deg, rgba(0,0,0,.92) 0%, rgba(0,0,0,.68) 52%, rgba(0,0,0,.22)),
      var(--hero-img) center/cover no-repeat;
  }

  .blog-index .service-hero h1 {
    max-width: 980px;
    font-size: 72px;
  }

  .blog-index .service-hero p {
    max-width: 710px;
  }

  .blog-editorial-intro {
    margin: -62px auto 58px;
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1.2fr .8fr;
    gap: 28px;
    align-items: stretch;
    padding: 30px;
    border: 1px solid rgba(201,161,74,.24);
    border-radius: 28px;
    background: rgba(255,253,248,.94);
    box-shadow: 0 28px 80px rgba(34,24,12,.13);
    backdrop-filter: blur(10px);
  }

  .blog-editorial-intro h2 {
    margin: 8px 0 12px;
    font-size: 42px;
  }

  .blog-editorial-intro p {
    margin: 0;
    max-width: 760px;
    color: #6d6256;
    text-align: left;
  }

  .blog-stats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .blog-stat {
    padding: 20px;
    border-radius: 18px;
    background: #0c0b09;
    color: #fff;
    box-shadow: inset 0 0 0 1px rgba(227,195,109,.22);
  }

  .blog-stat strong {
    display: block;
    color: #e3c36d;
    font-size: 28px;
    line-height: 1;
  }

  .blog-stat span {
    display: block;
    margin-top: 8px;
    color: #d9d0be;
    font-size: 14px;
  }

  .blog-topic-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 0 0 34px;
  }

  .blog-topic {
    padding: 10px 15px;
    border: 1px solid rgba(201,161,74,.34);
    border-radius: 999px;
    background: #fffdf8;
    color: #6e4f18;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: .08em;
    text-transform: uppercase;
  }

  .blog-index .blog-cards {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: stretch;
  }

  .blog-index .article-card {
    border-radius: 24px;
    border-color: rgba(201,161,74,.22);
    box-shadow: 0 18px 48px rgba(28,20,12,.08);
    transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
  }

  .blog-index .article-card:hover {
    transform: translateY(-6px);
    border-color: rgba(201,161,74,.66);
    box-shadow: 0 26px 70px rgba(28,20,12,.15);
  }

  .blog-index .article-card:first-child {
    grid-column: span 2;
    display: grid;
    grid-template-columns: .95fr 1fr;
  }

  .blog-index .article-card:first-child .article-cover {
    min-height: 100%;
  }

  .blog-index .article-card:first-child .article-cover-title {
    font-size: 34px;
  }

  .blog-index .article-card:first-child > .eyebrow,
  .blog-index .article-card:first-child > h3,
  .blog-index .article-card:first-child > p,
  .blog-index .article-card:first-child > .article-meta {
    margin-left: 32px;
    margin-right: 32px;
  }

  .blog-index .article-card:first-child > .eyebrow {
    align-self: end;
    margin-top: 34px;
  }

  .article-meta {
    margin: auto 28px 28px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
  }

  .article-meta span {
    padding: 7px 10px;
    border-radius: 999px;
    background: rgba(201,161,74,.1);
    color: #79591f;
    font-size: 12px;
    font-weight: 800;
  }

  .article-meta b {
    margin-left: auto;
    color: #9d762c;
    font-size: 13px;
    letter-spacing: .08em;
    text-transform: uppercase;
  }

  .article-summary {
    text-align: left;
    color: #5d554d;
    font-size: 21px;
    line-height: 1.55;
  }

  .article-author {
    margin: 28px 0 42px;
    padding: 20px 24px;
    border-left: 4px solid #c9a14a;
    border-radius: 0 16px 16px 0;
    background: #fff8e8;
  }

  .article-author strong,
  .article-author span {
    display: block;
  }

  .article-author strong {
    color: #1e1913;
    font-size: 20px;
  }

  .article-author span {
    margin-top: 4px;
    color: #746a5d;
  }

  .article-body-featured p {
    text-align: left;
  }

  .article-bibliography {
    margin: 22px 0 0;
    padding-left: 22px;
    color: #5f574e;
    font-size: 16px;
    line-height: 1.55;
  }

  .article-bibliography li + li {
    margin-top: 10px;
  }

  @media (max-width: 1100px) {
    .blog-editorial-intro,
    .blog-index .article-card:first-child {
      grid-template-columns: 1fr;
    }

    .blog-index .article-card:first-child {
      grid-column: span 1;
    }

    .blog-index .blog-cards {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 720px) {
    .blog-index .service-hero {
      padding: 82px 22px 78px;
    }

    .blog-index .service-hero h1 {
      font-size: 42px;
    }

    .blog-editorial-intro {
      margin-top: -42px;
      padding: 22px;
    }

    .blog-editorial-intro h2 {
      font-size: 32px;
    }

    .blog-stats,
    .blog-index .blog-cards {
      grid-template-columns: 1fr;
    }
  }

  .footer {
    position: relative;
    overflow: hidden;
    padding: 78px 48px 30px;
    background:
      radial-gradient(circle at 18% 0%, rgba(201,161,74,.14), transparent 32%),
      linear-gradient(180deg, #090806 0%, #030303 100%);
    border-top: 1px solid rgba(201,161,74,.35);
  }

  .footer:before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(90deg, transparent, rgba(227,195,109,.08), transparent);
  }

  .footer-grid {
    position: relative;
    padding: 38px;
    border: 1px solid rgba(201,161,74,.18);
    border-radius: 24px;
    background: rgba(255,255,255,.025);
    box-shadow: 0 24px 74px rgba(0,0,0,.34);
    gap: 30px;
    align-items: start;
  }

  .footer h3 {
    margin-top: 0;
    color: #f2d98c;
    font-size: 20px;
    line-height: 1.15;
  }

  .footer p {
    text-align: left;
    color: #d6cdbc;
    line-height: 1.55;
  }

  .footer-logo {
    margin-bottom: 18px;
    filter: drop-shadow(0 12px 28px rgba(201,161,74,.18));
  }

  .footer-brand p {
    max-width: 360px;
  }

  .footer-services > h3,
  .footer-contact > h3 {
    margin-bottom: 16px;
  }

  .footer-service-groups {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .footer-service-group {
    padding: 16px;
    border: 1px solid rgba(201,161,74,.16);
    border-radius: 16px;
    background: rgba(255,255,255,.035);
  }

  .footer-service-group h4 {
    margin: 0 0 10px;
    color: #fff8e5;
    font-size: 15px;
    letter-spacing: .1em;
    text-transform: uppercase;
  }

  .footer-service-group a {
    display: block;
    padding: 6px 0;
    color: #d8cba9;
    font-size: 15px;
    line-height: 1.25;
    border-top: 1px solid rgba(255,255,255,.06);
  }

  .footer-service-group a:first-of-type {
    border-top: 0;
  }

  .footer-links a,
  .social a {
    color: #ead8aa;
    transition: color .2s ease, transform .2s ease;
  }

  .footer-links a:hover,
  .footer-service-group a:hover,
  .social a:hover {
    color: #fff;
    transform: translateX(3px);
  }

  .social {
    margin-top: 22px;
  }

  .social a {
    padding: 8px 12px;
    border: 1px solid rgba(201,161,74,.24);
    border-radius: 999px;
    background: rgba(255,255,255,.035);
  }

  .footer .btn-gold {
    margin-top: 10px;
  }

  .footer-contact {
    padding: 24px;
    border: 1px solid rgba(201,161,74,.22);
    border-radius: 20px;
    background: rgba(255,253,248,.055);
  }

  .footer-contact p {
    margin: 0 0 14px;
  }

  .footer-contact .btn-gold {
    width: 100%;
    text-align: center;
    padding-left: 18px;
    padding-right: 18px;
  }

  .footer-bottom {
    position: relative;
    text-align: center;
    color: #a99f8d;
  }

  @media (max-width: 1100px) {
    .service-grid:has(.service-card:nth-child(5):last-child) {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (min-width: 820px) {
    .footer-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (min-width: 1180px) {
    .footer-grid {
      grid-template-columns: .86fr 1.55fr .82fr;
    }
  }

  @media (max-width: 720px) {
    .service-grid:has(.service-card:nth-child(5):last-child) {
      grid-template-columns: 1fr;
    }

    .service-card {
      padding: 22px;
    }

    .footer-grid {
      padding: 26px;
      grid-template-columns: 1fr;
    }

    .footer-service-groups,
    .footer-links.columns {
      grid-template-columns: 1fr;
    }
  }
`;
document.head.appendChild(visualStyle);

const footer = document.querySelector('.footer');
if (footer && !footer.classList.contains('footer-organized')) {
  footer.classList.add('footer-organized');

  const [brandColumn, servicesColumn, contactColumn] = footer.querySelectorAll('.footer-grid > div');
  brandColumn?.classList.add('footer-brand');
  servicesColumn?.classList.add('footer-services');
  contactColumn?.classList.add('footer-contact');

  const serviceLinksWrap = servicesColumn?.querySelector('.footer-links.columns');
  if (servicesColumn && serviceLinksWrap && !servicesColumn.querySelector('.footer-service-groups')) {
    const serviceLinks = [...serviceLinksWrap.querySelectorAll('a')].map(link => ({
      href: link.getAttribute('href') || '#',
      label: link.textContent.trim()
    }));

    const groups = [
      { title: 'Patrimônio', terms: ['inventario', 'usucapiao', 'regularizacao-imoveis', 'imobiliario-contratual'] },
      { title: 'Financeiro', terms: ['dividas-produtor', 'dividas-bancarias', 'revisao-contratos', 'consignado', 'tarifas'] },
      { title: 'Previdência e trabalho', terms: ['beneficios', 'limbo', 'rescisao'] },
      { title: 'Saúde e consumidor', terms: ['judicializacao', 'consumidor'] },
      { title: 'Indenizações', terms: ['acidentes', 'multas', 'danos-eletricos'] }
    ];

    const groupedHtml = groups.map(group => {
      const links = serviceLinks.filter(item => group.terms.some(term => item.href.toLowerCase().includes(term)));
      if (!links.length) return '';

      return `
        <div class="footer-service-group">
          <h4>${group.title}</h4>
          ${links.map(item => `<a href="${item.href}">${item.label}</a>`).join('')}
        </div>
      `;
    }).join('');

    servicesColumn.innerHTML = `
      <h3>Áreas de atuação</h3>
      <div class="footer-service-groups">${groupedHtml}</div>
    `;
  }
}

const articleThemes = [
  { key: 'patrimonio', label: 'Patrimonio', terms: ['inventario', 'usucapiao', 'regularizacao', 'imobiliario'] },
  { key: 'financeiro', label: 'Financeiro', terms: ['dividas', 'bancarias', 'contratos-bancarios', 'consignado', 'tarifas', 'produtor-rural'] },
  { key: 'previdencia', label: 'Previdencia', terms: ['previdenciarios', 'limbo', 'rescisao'] },
  { key: 'saude', label: 'Saude & Direitos', terms: ['saude', 'consumidor'] },
  { key: 'indenizacoes', label: 'Indenizacoes', terms: ['acidentes', 'cemig', 'copasa', 'danos-eletricos'] }
];

document.querySelectorAll('.article-card').forEach(card => {
  if (card.querySelector('.article-cover')) return;

  const href = (card.getAttribute('href') || '').toLowerCase();
  const title = card.querySelector('h3')?.textContent?.trim() || 'Artigo juridico';
  const theme = articleThemes.find(item => item.terms.some(term => href.includes(term))) || articleThemes[0];

  card.dataset.cover = theme.key;
  card.insertAdjacentHTML('afterbegin', `
    <div class="article-cover" aria-hidden="true">
      <span class="article-cover-kicker">${theme.label}</span>
      <strong class="article-cover-title">${title.split(':')[0]}</strong>
    </div>
  `);

  if (!card.querySelector('.article-meta')) {
    card.insertAdjacentHTML('beforeend', `
      <div class="article-meta">
        <span>Guia pratico</span>
        <span>5 min</span>
        <b>Ler artigo</b>
      </div>
    `);
  }
});

const isBlogIndex = /\/blog\/(?:index\.html)?$/.test(window.location.pathname);
const blogCards = [...document.querySelectorAll('.article-card')];

if (isBlogIndex && blogCards.length > 12) {
  document.body.classList.add('blog-index');

  const blogContainer = document.querySelector('.blog-cards')?.closest('.container');
  if (blogContainer && !document.querySelector('.blog-editorial-intro')) {
    blogContainer.insertAdjacentHTML('afterbegin', `
      <div class="blog-editorial-intro">
        <div>
          <span class="eyebrow">Biblioteca juridica</span>
          <h2>Conteudos para entender o risco antes de decidir.</h2>
          <p>Uma curadoria de temas recorrentes em patrimonio, recuperacao financeira, previdencia, saude e indenizacoes, organizada para ajudar o visitante a reconhecer o problema e procurar orientacao no momento certo.</p>
        </div>
        <div class="blog-stats" aria-label="Resumo do blog">
          <div class="blog-stat"><strong>${blogCards.length}</strong><span>artigos publicados</span></div>
          <div class="blog-stat"><strong>5</strong><span>areas juridicas</span></div>
        </div>
      </div>
      <div class="blog-topic-bar" aria-label="Temas do blog">
        <span class="blog-topic">Patrimonio</span>
        <span class="blog-topic">Financeiro</span>
        <span class="blog-topic">Previdencia</span>
        <span class="blog-topic">Saude & Direitos</span>
        <span class="blog-topic">Indenizacoes</span>
      </div>
    `);
  }
}

const serviceData = {
  'patrimonio': { icon: 'P', desc: 'Organize bens, documentos e direitos com seguranca.' },
  'financeiro': { icon: 'F', desc: 'Analise cobrancas, contratos e riscos patrimoniais.' },
  'previdencia': { icon: 'R', desc: 'Planeje beneficios e corrija negativas do INSS.' },
  'saude & direitos': { icon: 'S', desc: 'Atue contra negativas, abusos e bloqueios de acesso.' },
  'indenizacoes': { icon: 'I', desc: 'Busque reparacao por prejuizos e falhas de servico.' }
};

const normalizeText = value => value
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .trim();

document.querySelectorAll('.service-card').forEach(card => {
  const label = card.querySelector('span')?.textContent?.trim() || '';
  const data = serviceData[normalizeText(label)] || { icon: 'E', desc: 'Conheca a estrategia indicada para o seu caso.' };

  if (!card.querySelector('.service-top')) {
    const labelEl = card.querySelector('span');
    labelEl?.insertAdjacentHTML('beforebegin', `
      <div class="service-top">
        <i class="service-icon" aria-hidden="true">${data.icon}</i>
      </div>
    `);
  }

  if (!card.querySelector('.service-desc')) {
    card.querySelector('h3')?.insertAdjacentHTML('afterend', `<p class="service-desc">${data.desc}</p>`);
  }

  if (!card.querySelector('.service-more')) {
    card.insertAdjacentHTML('beforeend', '<em class="service-more">Ver detalhes</em>');
  }
});
