document.querySelectorAll('.menu-toggle').forEach(button => {
  button.addEventListener('click', () => document.querySelector('.nav').classList.toggle('open'));
});

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
  { key: 'patrimonio', label: 'Patrimônio', terms: ['inventario', 'usucapiao', 'regularizacao', 'imobiliario'] },
  { key: 'financeiro', label: 'Financeiro', terms: ['dividas', 'bancarias', 'contratos-bancarios', 'consignado', 'tarifas', 'produtor-rural'] },
  { key: 'previdencia', label: 'Previdência', terms: ['previdenciarios', 'limbo', 'rescisao'] },
  { key: 'saude', label: 'Saúde &amp; Direitos', terms: ['saude', 'consumidor'] },
  { key: 'indenizacoes', label: 'Indenizações', terms: ['acidentes', 'cemig', 'copasa', 'danos-eletricos'] }
];

document.querySelectorAll('.article-card').forEach(card => {
  if (card.querySelector('.article-cover')) return;

  const href = (card.getAttribute('href') || '').toLowerCase();
  const title = card.querySelector('h3')?.textContent?.trim() || 'Artigo jurídico';
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
        <span>Guia prático</span>
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
          <span class="eyebrow">Biblioteca jurídica</span>
          <h2>Conteúdos para entender o risco antes de decidir.</h2>
          <p>Uma curadoria de temas recorrentes em patrimônio, recuperação financeira, previdência, saúde e indenizações, organizada para ajudar o visitante a reconhecer o problema e procurar orientação no momento certo.</p>
        </div>
        <div class="blog-stats" aria-label="Resumo do blog">
          <div class="blog-stat"><strong>${blogCards.length}</strong><span>artigos publicados</span></div>
          <div class="blog-stat"><strong>5</strong><span>áreas jurídicas</span></div>
        </div>
      </div>
      <div class="blog-topic-bar" aria-label="Temas do blog">
        <span class="blog-topic">Patrimônio</span>
        <span class="blog-topic">Financeiro</span>
        <span class="blog-topic">Previdência</span>
        <span class="blog-topic">Saúde &amp; Direitos</span>
        <span class="blog-topic">Indenizações</span>
      </div>
    `);
  }
}

const serviceData = {
  'patrimonio': { icon: 'P', desc: 'Organize bens, documentos e direitos com segurança.' },
  'financeiro': { icon: 'F', desc: 'Analise cobranças, contratos e riscos patrimoniais.' },
  'previdencia': { icon: 'R', desc: 'Planeje benefícios e corrija negativas do INSS.' },
  'saude & direitos': { icon: 'S', desc: 'Atue contra negativas, abusos e bloqueios de acesso.' },
  'indenizacoes': { icon: 'I', desc: 'Busque reparação por prejuízos e falhas de serviço.' }
};

const normalizeText = value => value
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .trim();

document.querySelectorAll('.service-card').forEach(card => {
  const label = card.querySelector('span')?.textContent?.trim() || '';
  const data = serviceData[normalizeText(label)] || { icon: 'E', desc: 'Conheça a estratégia indicada para o seu caso.' };

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
