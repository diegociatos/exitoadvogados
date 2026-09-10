# Êxito Advogados — site

Site institucional e de captação da **Êxito Advogados**, escritório dedicado a pessoas físicas.
A marca é independente e não deve exibir vínculo com outras marcas ou grupos: o posicionamento é
de advocacia para o cidadão, com páginas por tese para capturar busca orgânica e gerar contato.

- **Produção:** https://exitoadvogados.com.br
- **Hospedagem:** Netlify, publicando a raiz do repositório. O domínio com `www` responde 301 para o
  domínio sem `www`, que é o canônico usado em todo o site.
- **Stack:** HTML, CSS e JavaScript puros. Não há build, dependências nem framework — abrir o
  arquivo já é ver a página.

## Como rodar localmente

```bash
python -m http.server 8899
```

Depois abra `http://127.0.0.1:8899`. Um servidor é necessário (em vez de abrir o arquivo direto)
porque o `404.html` e os ícones usam caminhos absolutos a partir da raiz.

## Estrutura

```
index.html            Home: hero, serviços por setor, método, formulário e artigos
diagnostico.html      Formulário longo de captação
obrigado.html         Confirmação de envio do formulário (noindex)
privacidade.html      Política de Privacidade (LGPD)
termos.html           Termos de Uso
404.html              Página de erro servida pelo Netlify em qualquer caminho inválido

teses/                24 páginas de serviço
  patrimonio · financeiro · previdencia · saude · indenizacoes    -> 5 hubs de setor
  inventario · usucapiao · regularizacao-imoveis · ...            -> 17 serviços
  inventario-usucapiao · saude-direitos                           -> legado, com 301

blog/                 index + 52 artigos
css/
  style.css           Base: variáveis, tipografia, header, hero, seções, footer
  landing.css         Layout específico das páginas de tese
  enhance.css         Camada de refinamento visual (ver "Cuidados" abaixo)
js/
  main.js             Menu mobile, agrupamento do rodapé, cards de serviço e de artigo
  analytics.js        Medição de conversão (ver "Analytics" abaixo)
images/               Assets do site em .webp + os PNGs originais, guardados como fonte
tools/                Scripts de manutenção
```

## Cuidados ao editar

**`css/enhance.css` precisa ser o último stylesheet do `<head>`.** Ele carrega 110 regras que
sobrescrevem `style.css` e `landing.css` de propósito. Se entrar antes de um dos dois, o layout
muda. Em toda página nova, a ordem é: `style.css`, depois `landing.css` (se for página de tese),
depois `enhance.css`.

**Imagens são servidas em `.webp`.** Os PNGs em `images/` são os originais de alta resolução,
mantidos como fonte para reencodar quando necessário — eles não são referenciados por nenhuma
página. O master do logotipo é `logo-horizontal-premium.png`; dele saem o logo do site, o favicon
e a imagem de compartilhamento.

**`images/`, `css/` e `js/` têm cache de um ano** (configurado em `netlify.toml`). Ao mudar o
*conteúdo* de um desses arquivos, mude também o nome (ex.: `style.css` → `style.v2.css`) e atualize
as referências, senão o visitante que já esteve no site continuará vendo a versão antiga.

**Toda página nova precisa de:** `<title>`, `<meta name="description">`, `<link rel="canonical">`,
bloco Open Graph, os links de ícone e o `enhance.css`. Copie o `<head>` de uma página do mesmo tipo
e ajuste. Depois rode os dois scripts de manutenção:

```bash
python tools/gerar-sitemap.py
python tools/checar-links.py
```

`gerar-sitemap.py` reescreve o `sitemap.xml` a partir dos arquivos que existem, pulando
automaticamente o que estiver marcado como `noindex`. `checar-links.py` confere se todo `href` e
`src` interno aponta para um arquivo real.

## Analytics

`js/analytics.js` está no ar e **inativo por escolha**: a constante `GA4_ID` no topo do arquivo está
vazia, então nada de terceiros é carregado e nenhum cookie é criado. Preencha com o ID do GA4
(formato `G-XXXXXXXXXX`) para ligar a medição.

Independente disso, os eventos já são empilhados em `window.dataLayer`, de onde um Google Tag
Manager futuro pode lê-los sem precisar tocar nas 83 páginas. Eventos disparados:

| Evento | Quando |
|---|---|
| `page_context` | Em toda visita, com a seção (home / tese / blog / institucional) |
| `whatsapp_click` | Clique em qualquer CTA de WhatsApp, identificando de onde partiu |
| `form_start` | Primeiro campo do formulário recebe foco |
| `form_submit` | Envio do formulário, com a área de interesse escolhida |
| `telefone_click` / `email_click` | Clique em `tel:` ou `mailto:` |
| `scroll_depth` | 25%, 50%, 75% e 100% da página — mede se as teses são lidas |

O arquivo respeita o sinal *Do Not Track* do navegador antes de carregar qualquer script externo.

## Formulários

Os dois formulários (`index.html` e `diagnostico.html`) usam **FormSubmit**, que entrega o conteúdo
por e-mail em `grupociatos@grupociatos.com.br`. Campos de controle já configurados: `_next`
(redireciona para `obrigado.html` após o envio), `_captcha=false`, `_template=table` e `_honey`
(armadilha anti-spam). Há caixa de consentimento obrigatória apontando para a Política de
Privacidade.

> O primeiro envio a partir de um domínio novo exige que a FormSubmit confirme o e-mail de destino.
> Se os formulários pararem de entregar, é o primeiro lugar a checar.

## Pendências de conteúdo

Estas não são falhas técnicas — são decisões de conteúdo que dependem do escritório:

1. **Os 52 artigos do blog são o mesmo texto repetido.** Comparados entre si, os corpos são de 97,8%
   a 99,8% idênticos: um modelo de ~3.200 palavras onde só o nome do tema muda. Estão marcados como
   `noindex` e fora do sitemap para não caracterizar conteúdo em escala perante o Google. Só
   `protecao-civil-saude-mental.html` tem texto próprio. Precisam ser reescritos ou removidos.
2. **As 3 perguntas frequentes são iguais nas 17 teses** ("Meu caso precisa ir para a Justiça?",
   "Posso falar com um advogado antes de decidir?", "Quanto tempo demora?"). Perguntas reais e
   específicas por tese valem mais e habilitam marcação `FAQPage`.
3. **Os 5 hubs de setor são páginas magras** — hero mais uma grade de cartões, sem texto. O conteúdo
   da antiga `teses/saude-direitos.html` (hoje com 301) é bom material para engordar o hub de saúde.
4. **Confirmar a razão social.** O rodapé, a Política de Privacidade e os Termos dizem "Garcia,
   Oliveira e Miranda Advogados Associados". O cadastro do grupo registra a sociedade de advogados
   como "Garcia, Oliveira e Silva Advogados Associados" (OAB/MG nº 1263). Se a Êxito for outra
   sociedade, é preciso o CNPJ e o número de registro dela na OAB.
5. **Página "Sobre" e página de contato com mapa** ainda não existem.
6. **Publicidade na advocacia.** O conteúdo atual está sóbrio, sem promessa de resultado nem
   honorário exposto. Manter esse critério ao escrever qualquer texto novo, conforme o Provimento
   nº 205/2021 do Conselho Federal da OAB.

## Contatos

Êxito Advogados — Rua Guaicuí, 715, salas 203 a 207, Luxemburgo, Belo Horizonte/MG, CEP 30380-342
WhatsApp (31) 97699-3871 · grupociatos@grupociatos.com.br
