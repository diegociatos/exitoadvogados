# Êxito Advogados — Site Premium

Site institucional e de conversão para a Êxito Advogados (nome fantasia de Garcia, Oliveira e Miranda Advogados Associados — OAB/MG nº 1263), marca do Grupo Ciatos voltada para pessoas físicas.

---

## 📁 Estrutura do Projeto

```
gom-site/
├── index.html                          # Homepage premium
├── sitemap.xml                         # Sitemap SEO (16 teses + blog)
├── robots.txt                          # Diretivas para crawlers
├── css/
│   └── style.css                       # Design system completo (~1900 linhas)
├── js/
│   └── main.js                         # Interações + Bot IA "Sofia"
├── images/
│   ├── logo-horizontal.png             # Header/light
│   ├── logo-vertical.png               # Outros usos
│   └── logo-branca.png                 # Hero/footer/dark
├── teses/
│   ├── judicializacao-saude.html       # Tese modelo 1 (Saúde)
│   └── consignado-indevido.html        # Tese modelo 2 (Financeiro)
└── blog/
    └── index.html                      # Listagem de artigos
```

---

## 🎨 Design System

**Paleta de cores (CSS variables em `:root`):**
- `--gom-black: #0a0a0a` — Preto principal
- `--gom-wine: #6b1e2a` — Vinho (vermelho da logo)
- `--gom-gold: #c9a961` — Dourado sofisticado
- `--gom-cream: #faf7f2` — Off-white de fundo

**Tipografia:**
- **Display:** Playfair Display (títulos)
- **Serif (corpo):** Cormorant Garamond (com fallback para Book Antiqua)
- **Sans:** Inter (UI, navegação, microcopy)

Toda a paleta e tipografia está centralizada em `css/style.css` no bloco `:root` — para mudanças globais, edite apenas lá.

---

## 🤖 Bot IA "Sofia"

Bot conversacional como SDR jurídico premium, implementado em JS puro (sem dependências). Fluxo em 3 etapas conforme briefing:

1. **Diagnóstico** — identifica o problema (financeiro, saúde, patrimônio, consignado, outro)
2. **Consciência** — mostra risco/urgência/oportunidade conforme tese
3. **Conversão** — captura nome + telefone, encaminha para WhatsApp oficial

**Fluxos implementados:** financial, health_inss, patrimony, consigned, other, urgent, qualify (popular), qualify_premium, getPhone, closing, whatsapp.

**Para expandir:** edite o objeto `botFlow` em `js/main.js`. Cada estado tem `message`, `followUp`, `options` (com `next` apontando para próximo estado) e `freeText: true` para entrada livre.

---

## 📞 WhatsApp Oficial

Número configurado em todos os CTAs: **+55 31 9769-9387**

URL base nos botões: `https://wa.me/5531976993871?text=...`

Cada CTA usa mensagem contextual (urgência diferente para saúde vs. consignado vs. consultoria geral).

---

## 🔍 SEO Implementado

✅ **Schema.org** — `LegalService` em todas as páginas + `FAQPage` nas teses
✅ **Open Graph** — todas as páginas
✅ **Meta description** otimizada por página
✅ **Sitemap.xml** com prioridades por tese
✅ **Robots.txt** configurado
✅ **Headings hierárquicos** (H1 > H2 > H3)
✅ **FAQs estruturadas** para Featured Snippets
✅ **URLs limpas e semânticas** (`/teses/judicializacao-saude.html`)
✅ **Alt text** em todas as imagens
✅ **Lazy loading**-ready

**Próximos passos de SEO (depois do lançamento):**
1. Implementar Google Analytics + Search Console
2. Adicionar Google Tag Manager
3. Configurar Google My Business para SEO local
4. Conectar com Bing Webmaster Tools
5. Adicionar reviews schema quando houver depoimentos verificados

---

## 📄 Páginas Pendentes para Lançamento Completo

**Críticas (lançamento):**
- [ ] 14 páginas de tese restantes (modelo: replicar `judicializacao-saude.html`)
- [ ] Página "Sobre" detalhada (sócios, equipe, história)
- [ ] Página de contato com formulário + mapa
- [ ] Página política de privacidade (LGPD)
- [ ] Página termos de uso

**Crescimento (pós-lançamento):**
- [ ] 8-12 artigos de blog reais (cluster semântico por tese)
- [ ] Páginas long-tail programáticas (ex: "advogado plano de saúde em Belo Horizonte", "advogado consignado em [bairro]")
- [ ] Cases de sucesso anonimizados
- [ ] Glossário jurídico (gera autoridade + cauda longa)

**Como replicar páginas de tese:**
1. Copie `teses/judicializacao-saude.html` ou `teses/consignado-indevido.html`
2. Atualize: `<title>`, `<meta description>`, `<meta keywords>`, OG tags
3. Substitua o conteúdo do `.tese-hero` e `.tese-content`
4. Adapte FAQs específicas da nova tese
5. Atualize o Schema.org `LegalService` e `FAQPage`
6. Adicione no `sitemap.xml`

---

## ⚡ Performance / Core Web Vitals

**Otimizações aplicadas:**
- CSS único e enxuto (sem frameworks)
- JS vanilla (sem React/jQuery)
- Fontes Google com `preconnect`
- Logos PNG otimizados
- Lazy-loading de animações via Intersection Observer
- Sem dependências externas pesadas

**Para garantir 90+ no PageSpeed:**
1. Comprimir os PNGs com TinyPNG ou converter para WebP
2. Adicionar atributo `loading="lazy"` em imagens abaixo da fold
3. Servir via CDN (Cloudflare é gratuito)
4. Habilitar HTTP/2 e Brotli no servidor
5. Configurar cache headers (1 ano para CSS/JS/imagens com hash)

---

## 🚀 Deploy Recomendado

**Opção 1 — Hospedagem tradicional (simples):**
- Subir todos os arquivos via FTP para a hospedagem (Locaweb, Hostgator, etc.)
- Configurar SSL/HTTPS
- Apontar domínio `gomadvogados.com.br`

**Opção 2 — Premium (recomendado):**
- Deploy na **Vercel** ou **Netlify** (grátis, com CDN global)
- Cloudflare para DNS + cache + WAF
- Performance imbatível, deploy contínuo via Git

**Opção 3 — WordPress (se preferir CMS):**
- Migrar estrutura para WordPress mantendo o design
- Plugins: RankMath SEO, WP Rocket, Schema Pro
- Cuidado: pode comprometer performance se mal configurado

---

## 📊 Métricas para Acompanhar

Após o lançamento, monitorar mensalmente:

**SEO:**
- Posicionamento de palavras-chave principais (use Semrush ou Ahrefs)
- Tráfego orgânico mensal
- CTR por página de tese
- Backlinks ganhos

**Conversão:**
- Cliques no botão WhatsApp (Google Analytics events)
- Mensagens recebidas via WhatsApp (taggear origem)
- Conversas iniciadas pelo bot Sofia
- Taxa de conversa→reunião→contrato

**Performance:**
- Core Web Vitals (PageSpeed Insights)
- Tempo de carregamento mobile
- Taxa de rejeição por página

---

## 🛠️ Manutenção e Próximas Iterações

**Mensal:**
- Publicar 2-4 artigos no blog (rotacionar entre as 5 verticais)
- Atualizar depoimentos quando houver
- Revisar metas e CTAs por dados

**Trimestral:**
- Auditoria SEO técnico
- Atualizar Schema.org com novos casos
- Otimizar imagens novas

**Anual:**
- Revisão visual e brand evolution
- Atualização do bot IA com novos fluxos baseados em conversas reais
- Adicionar funcionalidades (calculadoras jurídicas, simuladores, etc.)

---

## 📞 Contatos

**Escritório:**
Êxito Advogados Associados
Rua Guaicui, 715, Sala 203-207
Luxemburgo, Belo Horizonte/MG
+55 31 9769-9387

---

**Versão:** 1.0 (Lançamento)
**Data:** Maio/2026
