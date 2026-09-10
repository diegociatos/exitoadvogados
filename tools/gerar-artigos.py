# -*- coding: utf-8 -*-
"""Gera as paginas de artigo a partir dos arquivos em conteudo/artigos/*.md.

Cada artigo e um markdown com um cabecalho de metadados entre linhas de tres
tracos. O gerador cuida de <head>, dados estruturados, trilha de navegacao,
CTA e links internos -- quem escreve so precisa se preocupar com o texto.

    python tools/gerar-artigos.py

Convencoes que valem regra:
  * uma secao "## Perguntas frequentes" com "### pergunta" vira marcacao
    FAQPage automaticamente. So escreva ali pergunta que exista de fato na
    cabeca do cliente, e resposta que so aquele artigo poderia dar.
  * o campo `tese` liga o artigo a pagina de servico correspondente, que e
    para onde o CTA do meio e do fim do texto apontam.
"""
import re, os, glob, json, html

ROOT = 'https://exitoadvogados.com.br'
WHATS = ('https://wa.me/5531976993871?text=Ol%C3%A1%2C%20vim%20pelo%20site%20da%20'
         '%C3%8Axito%20Advogados%20e%20gostaria%20de%20um%20diagn%C3%B3stico.')

AREAS = {
    'patrimonio':   ('Patrimônio',            'teses/patrimonio.html'),
    'financeiro':   ('Financeiro',            'teses/financeiro.html'),
    'previdencia':  ('Previdência',           'teses/previdencia.html'),
    'saude':        ('Saúde & Direitos',      'teses/saude.html'),
    'indenizacoes': ('Indenizações',          'teses/indenizacoes.html'),
    'familia':      ('Família e Sucessões',   'teses/familia.html'),
    'trabalho':     ('Trabalho',              'teses/trabalho.html'),
    'consumidor':   ('Consumidor',            'teses/consumidor.html'),
}


# --------------------------------------------------------------- markdown
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def markdown(texto):
    """Subconjunto suficiente: h2, h3, paragrafo, lista, citacao e tabela."""
    saida, i = [], 0
    linhas = texto.split('\n')
    while i < len(linhas):
        l = linhas[i].rstrip()
        if not l.strip():
            i += 1
        elif l.startswith('### '):
            saida.append('<h3>%s</h3>' % inline(l[4:].strip())); i += 1
        elif l.startswith('## '):
            saida.append('<h2>%s</h2>' % inline(l[3:].strip())); i += 1
        elif l.startswith('> '):
            bloco = []
            while i < len(linhas) and linhas[i].startswith('> '):
                bloco.append(linhas[i][2:].strip()); i += 1
            saida.append('<blockquote><p>%s</p></blockquote>' % inline(' '.join(bloco)))
        elif re.match(r'^[-*] ', l):
            itens = []
            while i < len(linhas) and re.match(r'^[-*] ', linhas[i]):
                itens.append('<li>%s</li>' % inline(linhas[i][2:].strip())); i += 1
            saida.append('<ul>%s</ul>' % ''.join(itens))
        elif re.match(r'^\d+\. ', l):
            itens = []
            while i < len(linhas) and re.match(r'^\d+\. ', linhas[i]):
                itens.append('<li>%s</li>' % inline(re.sub(r'^\d+\. ', '', linhas[i]).strip())); i += 1
            saida.append('<ol>%s</ol>' % ''.join(itens))
        elif l.startswith('|'):
            linhas_tab = []
            while i < len(linhas) and linhas[i].startswith('|'):
                linhas_tab.append(linhas[i]); i += 1
            celulas = [[c.strip() for c in ln.strip('|').split('|')] for ln in linhas_tab]
            celulas = [c for c in celulas if not all(re.fullmatch(r':?-{2,}:?', x) for x in c)]
            cab, corpo = celulas[0], celulas[1:]
            t = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % inline(c) for c in cab)
            b = '<tbody>%s</tbody>' % ''.join(
                '<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in linha) for linha in corpo)
            saida.append('<div class="tabela-rolagem"><table>%s%s</table></div>' % (t, b))
        else:
            par = []
            while i < len(linhas) and linhas[i].strip() and not re.match(
                    r'^(#{2,3} |[-*] |\d+\. |> |\|)', linhas[i]):
                par.append(linhas[i].strip()); i += 1
            saida.append('<p>%s</p>' % inline(' '.join(par)))
    return ''.join(saida)


# ------------------------------------------------------------ metadados
def ler(caminho):
    bruto = open(caminho, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', bruto, re.S)
    if not m:
        raise SystemExit('sem cabecalho de metadados: %s' % caminho)
    meta = {}
    for linha in m.group(1).split('\n'):
        if not linha.strip():
            continue
        k, v = linha.split(':', 1)
        v = v.strip()
        chave = k.strip()
        if chave == 'extras':
            # 'slug=Titulo, slug=Titulo': so quebra na virgula que antecede outro slug=,
            # porque o titulo pode ter virgula ('Acidentes em Uber, 99 e Aplicativos')
            meta[chave] = [x.strip() for x in re.split(r',\s*(?=[\w-]+=)', v) if x.strip()]
        elif chave in ('relacionados', 'artigos', 'servicos'):
            meta[chave] = [x.strip() for x in v.split(',') if x.strip()]
        else:
            meta[chave] = v
    return meta, m.group(2).strip()


def faqs(corpo_html):
    """Extrai pergunta/resposta da secao de perguntas frequentes ja renderizada."""
    m = re.search(r'<h2>Perguntas frequentes</h2>(.*)$', corpo_html, re.S)
    if not m:
        return []
    trecho = re.split(r'<h2>', m.group(1))[0]
    pares = re.findall(r'<h3>(.*?)</h3>(.*?)(?=<h3>|$)', trecho, re.S)
    limpo = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()
    return [(limpo(p), limpo(r)) for p, r in pares if limpo(r)]


# --------------------------------------------------------------- template
base = open('index.html', encoding='utf-8').read()
CABECA = re.search(r'<header class="topbar">.*?</header>', base, re.S).group(0)
RODAPE = re.search(r'<footer class="footer">.*?</footer>', base, re.S).group(0)
CAUDA = base[base.index('</footer>') + len('</footer>'):]
for a, b in [('href="index.html"', 'href="../index.html"'),
             ('href="index.html#', 'href="../index.html#'),
             ('href="teses/', 'href="../teses/'),
             ('href="blog/', 'href="../blog/'),
             ('href="diagnostico.html"', 'href="../diagnostico.html"'),
             ('href="privacidade.html"', 'href="../privacidade.html"'),
             ('href="termos.html"', 'href="../termos.html"'),
             ('src="images/', 'src="../images/'),
             ('src="js/', 'src="../js/')]:
    CABECA, RODAPE, CAUDA = CABECA.replace(a, b), RODAPE.replace(a, b), CAUDA.replace(a, b)


def montar(meta, corpo_md, todos):
    slug = meta['slug']
    url = '%s/blog/%s.html' % (ROOT, slug)
    corpo = markdown(corpo_md)
    perguntas = faqs(corpo)
    area_nome, area_url = AREAS[meta['area']]

    esc = lambda s: html.escape(s, quote=True)
    titulo, desc = meta['titulo'], meta['descricao']

    ld = [{
        '@context': 'https://schema.org', '@type': 'BlogPosting',
        'headline': meta['h1'][:110], 'description': desc, 'inLanguage': 'pt-BR',
        'datePublished': meta['publicado'], 'dateModified': meta.get('atualizado', meta['publicado']),
        'mainEntityOfPage': url, 'image': ROOT + '/images/og-exito-advogados.jpg',
        'author': {'@type': 'Organization', 'name': 'Êxito Advogados', '@id': ROOT + '/#escritorio'},
        'publisher': {'@id': ROOT + '/#escritorio'},
        'about': meta.get('assunto', area_nome),
    }, {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': ROOT + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Conteúdo', 'item': ROOT + '/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': meta['h1'][:110], 'item': url},
        ]}]
    if perguntas:
        ld.append({
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': p,
                            'acceptedAnswer': {'@type': 'Answer', 'text': r}}
                           for p, r in perguntas]})

    cabeca = ''.join([
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>%s</title>' % esc(titulo),
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="stylesheet" href="../css/style.css">',
        '<link rel="stylesheet" href="../css/landing.css">',
        '<!-- seo:v2 -->',
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="Êxito Advogados">',
        '<meta property="og:locale" content="pt_BR">',
        '<meta property="og:title" content="%s">' % esc(titulo),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:image" content="%s/images/og-exito-advogados.jpg">' % ROOT,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="Êxito Advogados">',
        '<meta property="article:published_time" content="%s">' % meta['publicado'],
        '<meta property="article:modified_time" content="%s">' % meta.get('atualizado', meta['publicado']),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(titulo),
        '<meta name="twitter:description" content="%s">' % esc(desc),
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

    trilha = ('<nav class="trilha" aria-label="Você está em"><a href="../index.html">Início</a>'
              '<span aria-hidden="true">›</span><a href="../blog/index.html">Conteúdo</a>'
              '<span aria-hidden="true">›</span><a href="%s">%s</a></nav>'
              % ('../' + area_url, esc(area_nome)))

    # campo `tese`: liga o artigo (intencao de pesquisa) a pagina de servico (intencao de contratar)
    servico = ''
    if meta.get('tese'):
        alvo = 'teses/%s.html' % meta['tese']
        if os.path.exists(alvo):
            h1 = re.search(r'<h1>(.*?)</h1>', open(alvo, encoding='utf-8').read(), re.S)
            if h1:
                servico = ('<p class="artigo-cta-servico">Saiba como a Êxito atua: '
                           '<a href="../%s">%s</a>.</p>' % (alvo, h1.group(1)))

    cta = (('<aside class="artigo-cta"><span class="eyebrow">Próximo passo</span>'
           '<h2>%s</h2><p>%s</p>' + servico.replace('%', '%%') + '<div class="cta-actions">'
           '<a class="btn-gold" href="%s" target="_blank" rel="noopener">Falar com advogado</a>'
           '<a class="btn-outline" href="../diagnostico.html">Enviar meus dados</a>'
           '</div></aside>') % (esc(meta.get('cta_titulo', 'Quer saber se o seu caso tem caminho?')),
                               esc(meta.get('cta_texto',
                                   'Envie o que aconteceu e a equipe da Êxito indica quais '
                                   'documentos separar e qual o próximo passo.')),
                               WHATS))

    rel = [a for a in todos if a['slug'] in meta.get('relacionados', [])]
    relacionados = ''
    if rel:
        cards = ''.join(
            '<a class="article-card" href="%s.html"><span class="eyebrow">Artigo</span>'
            '<h3>%s</h3><p>%s</p></a>' % (r['slug'], esc(r['h1']), esc(r['descricao']))
            for r in rel)
        relacionados = ('<section class="section"><div class="container">'
                        '<div class="section-head"><span class="eyebrow">Continue lendo</span>'
                        '<h2>Sobre o mesmo problema.</h2></div>'
                        '<div class="blog-cards">%s</div></div></section>' % cards)

    artigo = ('<section class="section"><div class="container">%s'
              '<article class="article-body article-body-featured">'
              '<span class="eyebrow">%s</span><h1>%s</h1>'
              '<p class="article-summary">%s</p>'
              '<p class="article-data">Publicado em %s · atualizado em %s</p>'
              '%s%s</article></div></section>%s'
              % (trilha, esc(meta.get('eyebrow', area_nome)), esc(meta['h1']),
                 esc(meta['resumo']),
                 data_br(meta['publicado']), data_br(meta.get('atualizado', meta['publicado'])),
                 corpo, cta, relacionados))

    return cabeca + CABECA + artigo + RODAPE + CAUDA


MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']


def data_br(iso):
    a, m, d = iso.split('-')
    return '%d de %s de %s' % (int(d), MESES[int(m) - 1], a)


def atualizar_indice(artigos):
    """Coloca os artigos escritos a mao no topo da listagem do blog."""
    caminho = 'blog/index.html'
    t = open(caminho, encoding='utf-8').read()
    esc = lambda s: html.escape(s, quote=True)

    for meta in artigos:
        alvo = '%s.html' % meta['slug']
        # remove card anterior do mesmo artigo, para o script poder rodar de novo
        t = re.sub(r'<a class="article-card" href="%s">.*?</a>' % re.escape(alvo), '', t, flags=re.S)

    cards = ''.join(
        '<a class="article-card" href="%s.html"><span class="eyebrow">%s</span>'
        '<h3>%s</h3><p>%s</p></a>'
        % (m['slug'], esc(m.get('eyebrow', '')), esc(m['h1']), esc(m['resumo']))
        for m in sorted(artigos, key=lambda m: m['publicado'], reverse=True))

    t = t.replace('<div class="blog-cards">', '<div class="blog-cards">' + cards, 1)
    open(caminho, 'w', encoding='utf-8', newline='\n').write(t)
    print('blog/index.html: %d artigos no topo da listagem' % len(artigos))

    # home: a secao "Conteudo" mostra sempre os tres artigos mais recentes
    recentes = sorted(artigos, key=lambda m: (m['publicado'], m['slug']), reverse=True)[:3]
    cards_home = ''.join(
        '<a class="article-card" href="blog/%s.html"><span class="eyebrow">%s</span>'
        '<h3>%s</h3><p>%s</p></a>'
        % (m['slug'], esc(m.get('eyebrow', 'Artigo')), esc(m['h1']), esc(m['resumo']))
        for m in recentes)
    home = open('index.html', encoding='utf-8').read()
    home, trocou = re.subn(
        r'(<span class="eyebrow">Conteúdo</span><h2>[^<]*</h2><p>[^<]*</p></div>'
        r'<div class="blog-cards">).*?(</div></div></section>)',
        lambda m: m.group(1) + cards_home + m.group(2), home, count=1, flags=re.S)
    if trocou:
        open('index.html', 'w', encoding='utf-8', newline='\n').write(home)
        print('index.html: secao de artigos com os %d mais recentes' % len(recentes))


def main():
    caminhos = sorted(glob.glob('conteudo/artigos/*.md'))
    if not caminhos:
        raise SystemExit('nenhum artigo em conteudo/artigos/')
    artigos = []
    for c in caminhos:
        meta, corpo = ler(c)
        meta['_corpo'] = corpo
        artigos.append(meta)
    for meta in artigos:
        pagina = montar(meta, meta['_corpo'], artigos)
        destino = 'blog/%s.html' % meta['slug']
        open(destino, 'w', encoding='utf-8', newline='\n').write(pagina)
        palavras = len(re.sub(r'<[^>]+>', ' ', markdown(meta['_corpo'])).split())
        print('%-52s %5d palavras  %2d FAQ' % (destino, palavras,
                                               len(faqs(markdown(meta['_corpo'])))))
    atualizar_indice(artigos)
    print('\n%d artigos gerados' % len(artigos))


if __name__ == '__main__':
    main()
