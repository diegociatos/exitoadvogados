# -*- coding: utf-8 -*-
"""Gera as paginas-mae de cada area (teses/<area>.html) a partir de
conteudo/areas/*.md, listando os servicos daquela area.

O hub existe para dois publicos ao mesmo tempo: o buscador, que precisa de uma
pagina com texto de verdade sobre o tema amplo, e o visitante, que precisa
escolher rapido em qual caixa o problema dele cabe. Por isso: texto no topo,
cartoes no meio, duvidas no fim.

    python tools/gerar-hubs.py
"""
import re, os, glob, json, html
import importlib.util

_d = os.path.dirname(__file__)


def _carregar(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(_d, arquivo))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_art = _carregar('artigos', 'gerar-artigos.py')
_srv = _carregar('servicos', 'gerar-servicos.py')

markdown, inline, ler, AREAS, WHATS, ROOT = (
    _art.markdown, _art.inline, _art.ler, _art.AREAS, _art.WHATS, _art.ROOT)
CABECA, RODAPE, CAUDA = _art.CABECA, _art.RODAPE, _art.CAUDA
secoes, cartoes = _srv.secoes, _srv.cartoes
esc = lambda s: html.escape(s, quote=True)


def montar(meta, corpo, servicos):
    sec = secoes(corpo)
    area = meta['slug']
    area_nome = AREAS[area][0]
    url = '%s/teses/%s.html' % (ROOT, area)
    meus = [s for s in servicos if s['area'] == area]
    faq = cartoes(sec.get('Perguntas frequentes', ''))

    ld = [{
        '@context': 'https://schema.org', '@type': 'CollectionPage',
        'name': meta['h1'], 'description': meta['descricao'], 'url': url,
        'inLanguage': 'pt-BR', 'isPartOf': {'@id': ROOT + '/#site'},
        'about': area_nome,
        'mainEntity': {
            '@type': 'ItemList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': s['h1'],
                 'url': '%s/teses/%s.html' % (ROOT, s['slug'])}
                for i, s in enumerate(meus)]},
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': ROOT + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': area_nome, 'item': url}]}]
    if faq:
        ld.append({'@context': 'https://schema.org', '@type': 'FAQPage',
                   'mainEntity': [{'@type': 'Question', 'name': p,
                                   'acceptedAnswer': {'@type': 'Answer',
                                                      'text': re.sub(r'<[^>]+>', '', markdown(r_))}}
                                  for p, r_ in faq]})

    cabeca = ''.join([
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>%s</title>' % esc(meta['titulo']),
        '<meta name="description" content="%s">' % esc(meta['descricao']),
        '<link rel="stylesheet" href="../css/style.css">',
        '<link rel="stylesheet" href="../css/landing.css">',
        '<!-- seo:v2 -->',
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Êxito Advogados">',
        '<meta property="og:locale" content="pt_BR">',
        '<meta property="og:title" content="%s">' % esc(meta['titulo']),
        '<meta property="og:description" content="%s">' % esc(meta['descricao']),
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:image" content="%s/images/og-exito-advogados.jpg">' % ROOT,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="Êxito Advogados">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(meta['titulo']),
        '<meta name="twitter:description" content="%s">' % esc(meta['descricao']),
        '<meta name="twitter:image" content="%s/images/og-exito-advogados.jpg">' % ROOT,
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="icon" type="image/png" href="/images/favicon-512.png" sizes="512x512">',
        '<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">',
        '<meta name="theme-color" content="#080808">',
        '<link rel="stylesheet" href="../css/enhance.css">',
        '<!-- schema:v2 -->',
        ''.join('<script type="application/ld+json">%s</script>'
                % json.dumps(o, ensure_ascii=False, separators=(',', ':')) for o in ld),
        '</head><body>'])

    hero = ('<section class="service-hero" style="--hero-img:url(/images/%s.webp)">'
            '<div class="container"><span class="eyebrow">%s</span><h1>%s</h1><p>%s</p>'
            '<div class="actions">'
            '<a class="btn-gold" href="%s" target="_blank" rel="noopener">Falar com advogado</a>'
            '<a class="btn-outline" href="../diagnostico.html">Enviar dados do caso</a></div>'
            '</div></section>'
            % (meta.get('foto', 'equipe-trabalhando'), esc(area_nome), esc(meta['h1']),
               inline(meta['intro']), WHATS))

    trilha = ('<nav class="trilha trilha-servico" aria-label="Você está em">'
              '<a href="../index.html">Início</a><span aria-hidden="true">›</span>'
              '<span>%s</span></nav>' % esc(area_nome))

    texto = ('<section class="section"><div class="container">%s'
             '<div class="hub-texto">%s</div></div></section>'
             % (trilha, markdown(sec.get('Resumo', ''))))

    # servicos antigos, feitos a mao antes do sistema de conteudo, entram pelo
    # campo `extras: slug=Titulo`; a descricao vem do <meta> da propria pagina
    for item in meta.get('extras', []):
        slug_extra, _, titulo_extra = item.partition('=')
        pagina = open('teses/%s.html' % slug_extra.strip(), encoding='utf-8').read()
        d = re.search(r'<meta name="description" content="(.*?)"', pagina, re.S)
        meus.append({'slug': slug_extra.strip(), 'h1': titulo_extra.strip(),
                     'descricao': html.unescape(d.group(1)) if d else titulo_extra.strip()})

    # a classe service-desc impede o main.js de acrescentar uma segunda descricao
    cards = ''.join(
        '<a class="service-card" href="%s.html"><span>%s</span><h3>%s</h3>'
        '<p class="service-desc">%s</p></a>'
        % (s['slug'], esc(area_nome), esc(s['h1']), esc(s.get('resumo_card', s['descricao'])))
        for s in meus)
    grade = ('<section class="section"><div class="container">'
             '<div class="section-head"><span class="eyebrow">Escolha o seu caso</span>'
             '<h2>%s</h2><p>%s</p></div><div class="service-grid">%s</div></div></section>'
             % (esc(meta.get('titulo_grade', 'Frentes de atuação nesta área')),
                esc(meta.get('texto_grade', 'Cada página explica o problema, os sinais de '
                                            'atenção, os documentos que importam e o caminho '
                                            'jurídico possível.')),
                cards))

    faq_html = ''
    if faq:
        c = ''.join('<div class="faq-card"><b>%s</b>%s</div>' % (esc(p), markdown(r_))
                    for p, r_ in faq)
        faq_html = ('<section class="landing-section"><div class="landing-head">'
                    '<span class="eyebrow">Dúvidas frequentes</span>'
                    '<h2>O que mais perguntam sobre %s</h2></div>'
                    '<div class="faq-grid">%s</div></section>' % (esc(area_nome.lower()), c))

    fechamento = ('<section class="landing-section"><div class="landing-cta"><div>'
                  '<span class="eyebrow">Próximo passo</span><h2>%s</h2><p>%s</p></div>'
                  '<div class="cta-actions">'
                  '<a class="btn-gold" href="%s" target="_blank" rel="noopener">Falar com advogado</a>'
                  '<a class="btn-outline" href="../diagnostico.html">Enviar dados</a>'
                  '</div></div></section>'
                  % (esc(meta.get('cta_titulo', 'Não sabe em qual caixa o seu caso cabe?')),
                     esc(meta.get('cta_texto', 'Descreva a situação em poucas linhas. A equipe da '
                                               'Êxito identifica a frente correta e explica o que '
                                               'fazer primeiro.')),
                     WHATS))

    return cabeca + CABECA + hero + texto + grade + faq_html + fechamento + RODAPE + CAUDA


def main():
    servicos = []
    for c in sorted(glob.glob('conteudo/servicos/*.md')):
        m, _ = ler(c)
        servicos.append(m)
    caminhos = sorted(glob.glob('conteudo/areas/*.md'))
    if not caminhos:
        raise SystemExit('nenhuma area em conteudo/areas/')
    for c in caminhos:
        meta, corpo = ler(c)
        pagina = montar(meta, corpo, servicos)
        destino = 'teses/%s.html' % meta['slug']
        open(destino, 'w', encoding='utf-8', newline='\n').write(pagina)
        n = len([s for s in servicos if s['area'] == meta['slug']])
        print('%-34s %2d serviços' % (destino, n))
    print('\n%d hubs gerados' % len(caminhos))


if __name__ == '__main__':
    main()
