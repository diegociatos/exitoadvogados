# -*- coding: utf-8 -*-
"""Reconstroi menu, rodape, grade de servicos da home e o campo "area de
interesse" dos formularios a partir de uma unica lista: MAPA, abaixo.

Para incluir um servico novo no site inteiro, acrescente-o aqui e rode, nesta
ordem:

    python tools/atualizar-navegacao.py
    python tools/gerar-servicos.py
    python tools/gerar-hubs.py
    python tools/gerar-artigos.py

(as paginas geradas copiam cabecalho e rodape da index.html, por isso a
navegacao precisa ser atualizada primeiro)
"""
import re, glob, html

WHATS = ('https://wa.me/5531976993871?text=Ol%C3%A1%2C%20vim%20pelo%20site%20da%20'
         '%C3%8Axito%20Advogados%20e%20gostaria%20de%20um%20diagn%C3%B3stico.')

# (rotulo, hub, [(slug, titulo)])  -- o rotulo tambem e a chave de icone do main.js
MAPA = [
    ('Família e Sucessões', 'familia', [
        ('divorcio', 'Divórcio'),
        ('pensao-alimenticia', 'Pensão Alimentícia'),
        ('guarda-de-filhos', 'Guarda de Filhos'),
        ('uniao-estavel', 'União Estável'),
        ('inventario', 'Inventário'),
    ]),
    ('Trabalho', 'trabalho', [
        ('verbas-rescisorias', 'Verbas Rescisórias'),
        ('justa-causa', 'Reversão de Justa Causa'),
        ('horas-extras', 'Horas Extras'),
        ('assedio-moral', 'Assédio Moral'),
        ('acidente-de-trabalho', 'Acidente de Trabalho'),
        ('rescisao-indireta', 'Rescisão Indireta'),
    ]),
    ('Consumidor', 'consumidor', [
        ('nome-negativado-indevidamente', 'Nome Negativado Indevidamente'),
        ('superendividamento', 'Superendividamento'),
        ('golpe-pix-fraude-bancaria', 'Golpe do Pix e Fraude Bancária'),
        ('atraso-cancelamento-voo', 'Voo Atrasado ou Cancelado'),
        ('produto-com-defeito', 'Produto com Defeito'),
        ('direito-consumidor-premium', 'Consumo de Alto Valor'),
    ]),
    ('Financeiro', 'financeiro', [
        ('dividas-bancarias', 'Dívidas Bancárias'),
        ('revisao-contratos-bancarios', 'Revisão de Contratos Bancários'),
        ('consignado-indevido', 'Empréstimo Consignado Indevido'),
        ('tarifas-bancarias', 'Tarifas Bancárias Abusivas'),
        ('dividas-produtor-rural', 'Dívidas de Produtor Rural'),
    ]),
    ('Previdência', 'previdencia', [
        ('beneficios-previdenciarios', 'Benefícios do INSS'),
        ('limbo-previdenciario', 'Limbo Previdenciário'),
    ]),
    ('Saúde & Direitos', 'saude', [
        ('judicializacao-saude', 'Plano de Saúde e SUS'),
        ('erro-medico', 'Erro Médico'),
    ]),
    ('Patrimônio', 'patrimonio', [
        ('usucapiao', 'Usucapião'),
        ('regularizacao-imoveis', 'Regularização de Imóveis'),
        ('direito-imobiliario-contratual', 'Direito Imobiliário Contratual'),
    ]),
    ('Indenizações', 'indenizacoes', [
        ('acidentes-apps', 'Acidentes em Uber, 99 e Aplicativos'),
        ('multas-cemig-copasa', 'Multas CEMIG e COPASA'),
        ('danos-eletricos', 'Danos Elétricos e Energia'),
    ]),
]

ATALHOS = [('Família', 'familia'), ('Trabalho', 'trabalho'),
           ('Consumidor', 'consumidor'), ('INSS', 'previdencia')]

# servicos antigos que mudaram de area: a trilha de navegacao deles acompanha
MUDARAM = {'rescisao-indireta': ('Previdência', 'Trabalho', 'trabalho'),
           'direito-consumidor-premium': ('Saúde & Direitos', 'Consumidor', 'consumidor')}

e = lambda s: html.escape(s, quote=True)


def nav(p):
    grupos = ''.join(
        '<div class="mega-area"><a class="mega-area-titulo" href="%steses/%s.html">%s</a>%s</div>'
        % (p, hub, e(rotulo),
           ''.join('<a href="%steses/%s.html">%s</a>' % (p, s, e(t)) for s, t in servs))
        for rotulo, hub, servs in MAPA)
    atalhos = ''.join('<li class="nav-atalho"><a href="%steses/%s.html">%s</a></li>' % (p, h, e(r))
                      for r, h in ATALHOS)
    return ('<nav class="nav"><ul>'
            '<li><a href="%sindex.html">Início</a></li>'
            '<li class="nav-item-dropdown nav-areas">'
            '<a href="%sindex.html#servicos" class="nav-link">Áreas de atuação</a>'
            '<div class="mega-menu mega-areas"><div class="mega-areas-grade">%s</div></div></li>'
            '%s'
            '<li><a href="%sblog/index.html">Conteúdo</a></li>'
            '<li><a href="%sdiagnostico.html">Diagnóstico</a></li>'
            '<li><a class="btn-header" href="%s" target="_blank" rel="noopener">Falar com advogado</a></li>'
            '</ul></nav>' % (p, p, grupos, atalhos, p, p, WHATS))


def rodape_servicos(p):
    grupos = ''.join(
        '<div class="footer-service-group"><h4><a href="%steses/%s.html">%s</a></h4>%s</div>'
        % (p, hub, e(rotulo),
           ''.join('<a href="%steses/%s.html">%s</a>' % (p, s, e(t)) for s, t in servs))
        for rotulo, hub, servs in MAPA)
    return ('<div class="footer-services"><h3>Áreas de atuação</h3>'
            '<div class="footer-service-groups">%s</div></div>' % grupos)


def grade_home():
    setores = ''.join(
        '<div class="service-sector"><div class="sector-title">'
        '<a class="eyebrow" href="teses/%s.html">%s</a></div><div class="service-grid">%s</div></div>'
        % (hub, e(rotulo),
           ''.join('<a class="service-card" href="teses/%s.html"><span>%s</span><h3>%s</h3></a>'
                   % (s, e(rotulo), e(t)) for s, t in servs))
        for rotulo, hub, servs in MAPA)
    return setores


def opcoes():
    grupos = ''.join('<optgroup label="%s">%s</optgroup>'
                     % (e(rotulo), ''.join('<option>%s</option>' % e(t) for _, t in servs))
                     for rotulo, _, servs in MAPA)
    return '<option value="">Área de interesse</option>%s<option>Outro assunto</option>' % grupos


BRAND_ANTIGO = ('Advocacia estratégica para pessoas físicas, com foco em recuperação financeira, '
                'proteção patrimonial, saúde, previdência e indenizações.')
BRAND_NOVO = ('Advocacia para pessoas físicas: família, trabalho, consumidor, dívidas, INSS, '
              'saúde, patrimônio e indenizações.')

n = 0
for caminho in sorted(glob.glob('**/*.html', recursive=True)):
    rel = caminho.replace(chr(92), '/')
    t = open(caminho, encoding='utf-8').read()
    if '<header class="topbar">' not in t:
        continue                                   # pagina legada, redirecionada
    o = t
    p = '/' if rel == '404.html' else ('../' if '/' in rel else '')

    t = re.sub(r'<nav class="nav">.*?</nav>', lambda m: nav(p), t, count=1, flags=re.S)

    t = re.sub(r'<div( class="footer-services")?><h3>(?:Serviços|Áreas de atuação)</h3>'
               r'<div class="footer-(?:links columns|service-groups)">.*?</div></div>'
               r'(?=<div( class="footer-contact")?><h3>Contato</h3>)',
               lambda m: rodape_servicos(p), t, count=1, flags=re.S)
    t = t.replace(BRAND_ANTIGO, BRAND_NOVO)

    t = re.sub(r'(<select name="area"[^>]*>).*?(</select>)',
               lambda m: m.group(1) + opcoes() + m.group(2), t, flags=re.S)

    if rel == 'index.html':
        t = re.sub(r'(<section id="servicos" class="section"><div class="container">'
                   r'<div class="section-head">.*?</div>).*?(</div></section>)',
                   lambda m: m.group(1) + grade_home() + m.group(2), t, count=1, flags=re.S)

    slug = rel.rsplit('/', 1)[-1][:-5]
    if rel.startswith('teses/') and slug in MUDARAM:
        antigo, novo, hub = MUDARAM[slug]
        t = re.sub(r'"position":2,"name":"%s","item":"[^"]+"' % re.escape(antigo),
                   '"position":2,"name":"%s","item":"https://exitoadvogados.com.br/teses/%s.html"'
                   % (novo, hub), t)
        t = t.replace('<span class="eyebrow">%s</span><h1>' % e(antigo),
                      '<span class="eyebrow">%s</span><h1>' % e(novo), 1)

    if t != o:
        open(caminho, 'w', encoding='utf-8', newline='\n').write(t)
        n += 1

total = sum(len(s) for _, _, s in MAPA)
print('%d paginas atualizadas | %d areas, %d servicos no menu' % (n, len(MAPA), total))
