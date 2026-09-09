/* Medicao de conversao do site da Exito Advogados.
 *
 * COMO ATIVAR: informe o ID do GA4 na constante abaixo (formato G-XXXXXXXXXX).
 * Enquanto ela estiver vazia o arquivo nao carrega nada de terceiros e nao usa
 * cookie -- os eventos ficam apenas em window.dataLayer, de onde um Google Tag
 * Manager futuro pode le-los sem precisar mexer nas 80 paginas do site.
 */
(function () {
  'use strict';

  var GA4_ID = ''; // <- ex.: 'G-ABC1234567'

  window.dataLayer = window.dataLayer || [];
  var push = function (nome, dados) {
    window.dataLayer.push(Object.assign({ event: nome }, dados || {}));
    if (window.gtag) window.gtag('event', nome, dados || {});
  };

  // Respeita "nao me rastreie" do navegador antes de carregar qualquer script externo.
  var recusou = navigator.doNotTrack === '1' || window.doNotTrack === '1';

  if (GA4_ID && !recusou) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA4_ID, { anonymize_ip: true });
  }

  // Em que tipo de pagina o visitante esta -- permite comparar teses entre si.
  var caminho = window.location.pathname;
  var secao = (caminho === '/' || caminho === '/index.html') ? 'home'
    : caminho.indexOf('/teses/') === 0 ? 'tese'
    : caminho.indexOf('/blog/') === 0 ? 'blog'
    : 'institucional';
  var pagina = caminho.split('/').pop().replace('.html', '') || 'home';

  push('page_context', { secao: secao, pagina: pagina });

  // --- Cliques que valem dinheiro -------------------------------------------
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';

    if (href.indexOf('wa.me') > -1 || href.indexOf('api.whatsapp') > -1) {
      var origem = a.classList.contains('floating-whats') ? 'botao-flutuante'
        : a.classList.contains('btn-header') ? 'cabecalho'
        : a.closest('.hero') ? 'hero'
        : a.closest('.cta-panel') ? 'painel-cta'
        : a.closest('.footer') ? 'rodape'
        : 'corpo';
      push('whatsapp_click', { secao: secao, pagina: pagina, origem: origem });
    } else if (href.indexOf('tel:') === 0) {
      push('telefone_click', { secao: secao, pagina: pagina });
    } else if (href.indexOf('mailto:') === 0) {
      push('email_click', { secao: secao, pagina: pagina });
    }
  });

  // --- Formulario: quem comecou e quem terminou -----------------------------
  document.querySelectorAll('form').forEach(function (form) {
    var iniciou = false;
    form.addEventListener('focusin', function () {
      if (iniciou) return;
      iniciou = true;
      push('form_start', { secao: secao, pagina: pagina });
    });
    form.addEventListener('submit', function () {
      var area = form.querySelector('[name="area"]');
      push('form_submit', {
        secao: secao,
        pagina: pagina,
        area_interesse: area ? area.value : ''
      });
    });
  });

  // --- Profundidade de leitura (mede se as teses sao lidas de fato) ---------
  var marcos = [25, 50, 75, 100];
  var vistos = {};
  var medir = function () {
    var alturaDoc = document.documentElement.scrollHeight - window.innerHeight;
    if (alturaDoc <= 0) return;
    var pct = (window.scrollY / alturaDoc) * 100;
    marcos.forEach(function (m) {
      if (pct >= m && !vistos[m]) {
        vistos[m] = true;
        push('scroll_depth', { secao: secao, pagina: pagina, percentual: m });
      }
    });
  };
  var agendado = false;
  window.addEventListener('scroll', function () {
    if (agendado) return;
    agendado = true;
    requestAnimationFrame(function () { agendado = false; medir(); });
  }, { passive: true });
})();
