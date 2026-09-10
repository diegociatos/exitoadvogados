# -*- coding: utf-8 -*-
"""Gera as paginas de servico (teses/) a partir de conteudo/servicos/*.md.

A pagina de servico e onde a busca transacional converte -- quem procura
"advogado pensao alimenticia" quer contratar, nao ler. Por isso ela e curta no
topo, especifica no meio e termina em CTA.

    python tools/gerar-servicos.py

O markdown usa secoes de nome fixo. O que muda de servico para servico e o
texto; o esqueleto e os blocos sobre o escritorio sao os mesmos, de proposito.

    ## Resumo                 paragrafo de abertura do corpo
    ## Quando procurar        tres cartoes, um "### titulo" + paragrafo cada
    ## Sinais de atencao      lista simples, vira as pills
    ## O que esta em jogo     paragrafo + tres "### titulo" + paragrafo
    ## Documentos             "### titulo" + paragrafo, quantos precisar
    ## Perguntas frequentes   "### pergunta" + resposta -> vira FAQPage
"""
import re, os, glob, json, html
import importlib.util

_spec = importlib.util.spec_from_file_location(
    'artigos', os.path.join(os.path.dirname(__file__), 'gerar-artigos.py'))
_art = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_art)

markdown, inline, ler, AREAS, WHATS, ROOT = (
    _art.markdown, _art.inline, _art.ler, _art.AREAS, _art.WHATS, _art.ROOT)

CABECA, RODAPE, CAUDA = _art.CABECA, _art.RODAPE, _art.CAUDA
esc = lambda s: html.escape(s, quote=True)


def secoes(corpo):
    """Quebra o markdown em {titulo da secao: texto}."""
    partes = re.split(r'^## ', corpo, flags=re.M)
    fora = {}
    for p in partes[1:]:
        nome, _, resto = p.partition('\n')
        fora[nome.strip()] = resto.strip()
    return fora


def cartoes(texto):
    """Le blocos '### titulo' + paragrafo e devolve [(titulo, texto)]."""
    pares = re.findall(r'^### (.+?)\n(.*?)(?=^### |\Z)', texto, re.S | re.M)
    return [(t.strip(), re.sub(r'\s+', ' ', c).strip()) for t, c in pares]


def antes_dos_cartoes(texto):
    return re.sub(r'\s+', ' ', re.split(r'^### ', texto, flags=re.M)[0]).strip()


def montar(meta, corpo, servicos):
    sec = secoes(corpo)
    slug, area = meta['slug'], meta['area']
    area_nome, area_url = AREAS[area]
    url = '%s/teses/%s.html' % (ROOT, slug)
    foto = meta.get('foto', 'atendimento-cliente')

    quando = cartoes(sec.get('Quando procurar', ''))
    sinais = re.findall(r'^[-*] (.+)$', sec.get('Sinais de atenção', ''), re.M)
    jogo_intro = antes_dos_cartoes(sec.get('O que está em jogo', ''))
    jogo = cartoes(sec.get('O que está em jogo', ''))
    docs = cartoes(sec.get('Documentos', ''))
    faq = cartoes(sec.get('Perguntas frequentes', ''))

    ld = [{
        '@context': 'https://schema.org', '@type': 'LegalService',
        '@id': url + '#servico',
        'name': 'Êxito Advogados — ' + meta['h1'],
        'description': meta['descricao'], 'url': url,
        'image': ROOT + '/images/og-exito-advogados.jpg',
        'telephone': '+55 31 97699-3871',
        'address': {'@type': 'PostalAddress',
                    'streetAddress': 'Rua Guaicuí, 715, salas 203 a 207',
                    'addressLocality': 'Belo Horizonte', 'addressRegion': 'MG',
                    'postalCode': '30380-342', 'addressCountry': 'BR'},
        'areaServed': [{'@type': 'City', 'name': 'Belo Horizonte'},
                       {'@type': 'State', 'name': 'Minas Gerais'}],
        'serviceType': meta['h1'], 'availableLanguage': 'pt-BR',
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': ROOT + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': area_nome,
             'item': '%s/%s' % (ROOT, area_url)},
            {'@type': 'ListItem', 'position': 3, 'name': meta['h1'], 'item': url},
        ]}]
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

    botoes = ('<div class="actions">'
              '<a class="btn-gold" href="%s" target="_blank" rel="noopener">Falar com advogado</a>'
              '<a class="btn-outline" href="../diagnostico.html">Enviar dados do caso</a></div>' % WHATS)

    hero = ('<section class="service-hero" style="--hero-img:url(/images/%s.webp)">'
            '<div class="container"><span class="eyebrow">%s</span><h1>%s</h1><p>%s</p>%s</div>'
            '</section>' % (foto, esc(area_nome), esc(meta['h1']), inline(meta['intro']), botoes))

    trilha = ('<nav class="trilha trilha-servico" aria-label="Você está em">'
              '<a href="../index.html">Início</a><span aria-hidden="true">›</span>'
              '<a href="../%s">%s</a><span aria-hidden="true">›</span>'
              '<span>%s</span></nav>' % (area_url, esc(area_nome), esc(meta['h1'])))

    minis = ''.join('<div class="mini"><h3>%s</h3><p>%s</p></div>' % (esc(t), inline(c))
                    for t, c in quando)
    pills = ''.join('<span class="pill">%s</span>' % inline(s) for s in sinais)

    corpo_principal = (
        '<section class="section"><div class="container">%s<div class="content-grid"><main>'
        '<span class="eyebrow">Atuação</span><h2>Como a Êxito atua em %s</h2>%s'
        '%s'
        '%s'
        '</main><aside><div class="cta-panel"><h3>Diagnóstico do seu caso</h3>'
        '<p>Conte o que aconteceu. A equipe avalia se existe caminho jurídico, quais documentos '
        'separar e o que esperar de prazo.</p>'
        '<a class="btn-gold" href="%s" target="_blank" rel="noopener">WhatsApp</a><br><br>'
        '<a class="btn-outline" href="../diagnostico.html">Prefiro formulário</a>'
        '</div></aside></div></div></section>'
        % (trilha, esc(meta['h1']), markdown(sec.get('Resumo', '')),
           ('<div class="mini-grid">%s</div>' % minis) if minis else '',
           ('<h2>Sinais de atenção</h2><div class="pill-list">%s</div>' % pills) if pills else '',
           WHATS))

    jogo_html = ''
    if jogo:
        cards = ''.join('<div class="value-card"><b>%s</b><p>%s</p></div>' % (esc(t), inline(c))
                        for t, c in jogo)
        jogo_html = ('<section class="landing-section"><div class="landing-head">'
                     '<span class="eyebrow">Por que agir agora</span>'
                     '<h2>O que está em jogo</h2><p>%s</p></div>'
                     '<div class="value-grid">%s</div></section>' % (inline(jogo_intro), cards))

    processo = (
        '<section class="landing-section landing-dark"><div class="landing-head">'
        '<span class="eyebrow">Como funciona</span>'
        '<h2>De dúvida a estratégia, em quatro etapas.</h2></div>'
        '<div class="process-grid">'
        '<div class="process-step"><span>1</span><b>Entendimento inicial</b>'
        '<p>Você conta o que aconteceu, sem formalidade e sem compromisso.</p></div>'
        '<div class="process-step"><span>2</span><b>Análise documental</b>'
        '<p>Conferimos provas, contratos, comunicações, prazos e fragilidades.</p></div>'
        '<div class="process-step"><span>3</span><b>Estratégia jurídica</b>'
        '<p>Apresentamos o caminho possível, o que esperar e o que pode dar errado.</p></div>'
        '<div class="process-step"><span>4</span><b>Condução do caso</b>'
        '<p>Você acompanha cada passo com comunicação direta e linguagem clara.</p></div>'
        '</div></section>')

    docs_html = ''
    if docs:
        cards = ''.join('<div class="document-card"><b>%s</b><p>%s</p></div>' % (esc(t), inline(c))
                        for t, c in docs)
        docs_html = ('<section class="landing-section"><div class="landing-head">'
                     '<span class="eyebrow">Provas e documentos</span>'
                     '<h2>O que separar antes da primeira conversa</h2>'
                     '<p>Quanto mais completo o material, mais preciso o diagnóstico — e menor a '
                     'chance de entrar em uma medida sem chance real.</p></div>'
                     '<div class="document-grid">%s</div></section>' % cards)

    faq_html = ''
    if faq:
        cards = ''.join('<div class="faq-card"><b>%s</b>%s</div>' % (esc(p), markdown(r_))
                        for p, r_ in faq)
        faq_html = ('<section class="landing-section"><div class="landing-head">'
                    '<span class="eyebrow">Dúvidas frequentes</span>'
                    '<h2>O que as pessoas perguntam sobre %s</h2></div>'
                    '<div class="faq-grid">%s</div></section>' % (esc(meta['h1'].lower()), cards))

    rel = [s for s in servicos if s['slug'] in meta.get('relacionados', [])]
    rel_html = ''
    if rel:
        cards = ''.join('<a class="service-card" href="%s.html"><span>%s</span><h3>%s</h3></a>'
                        % (r['slug'], esc(AREAS[r['area']][0]), esc(r['h1'])) for r in rel)
        rel_html = ('<section class="section"><div class="container">'
                    '<div class="section-head"><span class="eyebrow">Também pode ser o seu caso</span>'
                    '<h2>Serviços próximos deste.</h2></div>'
                    '<div class="service-grid">%s</div></div></section>' % cards)

    artigos_html = ''
    if meta.get('artigos'):
        cards = ''.join('<a class="article-card" href="../blog/%s.html">'
                        '<span class="eyebrow">Artigo</span><h3>%s</h3></a>'
                        % (a, esc(_titulo_artigo(a))) for a in meta['artigos'])
        artigos_html = ('<section class="section"><div class="container">'
                        '<div class="section-head"><span class="eyebrow">Leia antes de decidir</span>'
                        '<h2>Conteúdo sobre este tema.</h2></div>'
                        '<div class="blog-cards">%s</div></div></section>' % cards)

    fechamento = ('<section class="landing-section"><div class="landing-cta"><div>'
                  '<span class="eyebrow">Próximo passo</span><h2>%s</h2><p>%s</p></div>'
                  '<div class="cta-actions">'
                  '<a class="btn-gold" href="%s" target="_blank" rel="noopener">Falar com advogado</a>'
                  '<a class="btn-outline" href="../diagnostico.html">Enviar dados</a>'
                  '</div></div></section>'
                  % (esc(meta.get('cta_titulo', 'Quer saber se existe caminho no seu caso?')),
                     esc(meta.get('cta_texto',
                         'Envie o que aconteceu e a equipe da Êxito responde com uma leitura '
                         'inicial do cenário e dos documentos que importam.')),
                     WHATS))

    return (cabeca + CABECA + hero + corpo_principal + jogo_html + processo
            + docs_html + faq_html + rel_html + artigos_html + fechamento + RODAPE + CAUDA)


_cache_artigos = {}


def _titulo_artigo(slug):
    if not _cache_artigos:
        for c in glob.glob('conteudo/artigos/*.md'):
            m, _ = ler(c)
            _cache_artigos[m['slug']] = m['h1']
    return _cache_artigos.get(slug, slug.replace('-', ' ').capitalize())


def main():
    caminhos = sorted(glob.glob('conteudo/servicos/*.md'))
    if not caminhos:
        raise SystemExit('nenhum servico em conteudo/servicos/')
    servicos = []
    for c in caminhos:
        meta, corpo = ler(c)
        meta['_corpo'] = corpo
        servicos.append(meta)
    for meta in servicos:
        pagina = montar(meta, meta['_corpo'], servicos)
        destino = 'teses/%s.html' % meta['slug']
        open(destino, 'w', encoding='utf-8', newline='\n').write(pagina)
        palavras = len(re.sub(r'<[^>]+>', ' ', markdown(meta['_corpo'])).split())
        print('%-44s %5d palavras' % (destino, palavras))
    print('\n%d servicos gerados' % len(servicos))


if __name__ == '__main__':
    main()
