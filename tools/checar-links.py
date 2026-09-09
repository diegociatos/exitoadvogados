# -*- coding: utf-8 -*-
"""Confere se todo href/src interno do site aponta para um arquivo que existe.
Rode da raiz do projeto: python tools/checar-links.py"""
import re, glob, os, urllib.parse

quebrados = []
for path in sorted(glob.glob('**/*.html', recursive=True)):
    rel = path.replace(chr(92), '/')
    base = os.path.dirname(rel)
    conteudo = open(path, encoding='utf-8').read()
    for _, valor in re.findall(r'(href|src)="([^"]+)"', conteudo):
        if re.match(r'https?:|mailto:|tel:|#|data:', valor):
            continue
        alvo = urllib.parse.unquote(valor.split('#')[0].split('?')[0])
        if not alvo:
            continue
        p = alvo[1:] if alvo.startswith('/') else (base + '/' + alvo if base else alvo)
        p = os.path.normpath(p).replace(chr(92), '/')
        if not os.path.exists(p):
            quebrados.append((rel, valor, p))

print('links internos quebrados:', len(quebrados))
for origem, valor, procurado in quebrados[:40]:
    print('   %-46s -> %-34s (procurado em %s)' % (origem, valor, procurado))
