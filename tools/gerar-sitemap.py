# -*- coding: utf-8 -*-
"""Regera o sitemap a partir dos arquivos que existem de fato, excluindo o que
esta marcado como noindex. Rode de novo sempre que criar ou remover paginas."""
import glob, re, os
from datetime import date

ROOT = 'https://exitoadvogados.com.br'
HOJE = date.today().isoformat()

EXCLUIR = {'404.html'}

HUBS = {'teses/patrimonio.html', 'teses/financeiro.html', 'teses/previdencia.html',
        'teses/saude.html', 'teses/indenizacoes.html'}


def prioridade(rel):
    if rel == 'index.html':
        return '1.0', 'weekly'
    if rel in HUBS:
        return '0.9', 'monthly'
    if rel == 'diagnostico.html':
        return '0.8', 'monthly'
    if rel.startswith('teses/'):
        return '0.8', 'monthly'
    if rel == 'blog/index.html':
        return '0.7', 'weekly'
    if rel.startswith('blog/'):
        return '0.6', 'monthly'
    return '0.3', 'yearly'


entradas = []
pulados = []
for path in sorted(glob.glob('**/*.html', recursive=True)):
    rel = path.replace('\\', '/')
    if rel in EXCLUIR:
        pulados.append((rel, 'nao indexavel'))
        continue
    t = open(path, encoding='utf-8').read()
    if re.search(r'<meta name="robots" content="[^"]*noindex', t):
        pulados.append((rel, 'noindex'))
        continue
    loc = ROOT + '/' if rel == 'index.html' else ROOT + '/' + rel
    pri, freq = prioridade(rel)
    entradas.append((loc, pri, freq))

entradas.sort(key=lambda e: (-float(e[1]), e[0]))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pri, freq in entradas:
    out += ['  <url>',
            '    <loc>%s</loc>' % loc,
            '    <lastmod>%s</lastmod>' % HOJE,
            '    <changefreq>%s</changefreq>' % freq,
            '    <priority>%s</priority>' % pri,
            '  </url>']
out.append('</urlset>')
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')

print('sitemap.xml: %d URLs' % len(entradas))
for rel, motivo in pulados:
    print('  fora: %-38s (%s)' % (rel, motivo))
