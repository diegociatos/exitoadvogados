# Êxito Advogados — site

Site institucional e de captação da **Êxito Advogados**, escritório dedicado a pessoas físicas.
A marca é independente e não deve exibir vínculo com outras marcas ou grupos: o posicionamento é
de advocacia para o cidadão, com páginas por tese para capturar busca orgânica e gerar contato.

- **Produção:** https://exitoadvogados.com.br
- **Hospedagem:** Netlify, publicando a raiz do repositório. O domínio com `www` responde 301 para o
  domínio sem `www`, que é o canônico usado em todo o site.
- **Stack:** HTML, CSS e JavaScript puros. Não há build no servidor nem dependências. Os scripts em
  `tools/` rodam na sua máquina, com Python 3, e gravam HTML pronto no repositório.

## Como rodar localmente

```bash
python -m http.server 8899
```

Depois abra `http://127.0.0.1:8899`. Um servidor é necessário (em vez de abrir o arquivo direto)
porque o `404.html`, os ícones e as imagens de fundo usam caminhos absolutos a partir da raiz.

## Arquitetura de conteúdo

O site é organizado em três camadas, cada uma com um papel de busca diferente:

| Camada | Onde fica | Intenção de busca | Exemplo |
|---|---|---|---|
| Hub de área | `teses/<area>.html` | Tema amplo | "advogado de família BH" |
| Página de serviço | `teses/<servico>.html` | Quer contratar | "advogado pensão alimentícia" |
| Artigo | `blog/<artigo>.html` | Quer entender o problema | "pensão atrasada o que fazer" |

Os artigos apontam para a página de serviço (campo `tese`), que aponta para o hub, que aponta para
todos os serviços da área. É essa malha de links internos que distribui autoridade entre as páginas.

As **8 áreas** e os **32 serviços** exibidos no menu, no rodapé, na home e no campo "área de
interesse" dos formulários estão definidos em um único lugar: a lista `MAPA` em
`tools/atualizar-navegacao.py`.

## Como publicar conteúdo novo

Todo conteúdo novo nasce em markdown, dentro de `conteudo/`, e é convertido em HTML pelos scripts:

```
conteudo/
  areas/       um arquivo por hub de área       -> tools/gerar-hubs.py
  servicos/    um arquivo por página de serviço -> tools/gerar-servicos.py
  artigos/     um arquivo por artigo            -> tools/gerar-artigos.py
```

Cada arquivo começa com um bloco de metadados entre linhas `---` (título, descrição, área,
relacionados) e segue com o texto. Use qualquer arquivo existente como modelo. As convenções que
importam:

- Uma seção `## Perguntas frequentes` com `### pergunta` vira marcação `FAQPage` automaticamente.
  Escreva ali só perguntas reais e específicas daquele tema.
- No artigo, `tese:` liga o texto à página de serviço correspondente.
- No serviço, `artigos:` lista os artigos que aparecem no fim da página.
- No hub, `extras: slug=Título` inclui na grade uma página de serviço antiga, feita à mão.

Depois de escrever ou alterar, rode na ordem:

```bash
python tools/atualizar-navegacao.py
python tools/gerar-servicos.py
python tools/gerar-hubs.py
python tools/gerar-artigos.py
python tools/gerar-sitemap.py
python tools/checar-links.py
```

A navegação vem primeiro porque as páginas geradas copiam cabeçalho e rodapé da `index.html`. O
gerador de artigos também atualiza a listagem do blog e os três artigos em destaque na home.

## Cuidados ao editar

**`css/enhance.css` precisa ser o último stylesheet do `<head>`.** Ele sobrescreve `style.css` e
`landing.css` de propósito. As páginas geradas já saem na ordem certa.

**Imagens são servidas em `.webp`.** Os PNGs em `images/` são os originais de alta resolução,
mantidos como fonte. O master do logotipo é `logo-horizontal-premium.png`; dele saem o logo do
site, o favicon e a imagem de compartilhamento.

**`images/`, `css/` e `js/` têm cache de um ano** (configurado em `netlify.toml`). Ao mudar o
*conteúdo* de um desses arquivos depois que o site estiver no ar com essa configuração, mude também
o nome (ex.: `style.css` → `style.v2.css`) e atualize as referências, senão quem já visitou o site
continuará vendo a versão antiga.

## Analytics

`js/analytics.js` está no ar e **inativo por escolha**: a constante `GA4_ID` no topo do arquivo está
vazia, então nada de terceiros é carregado e nenhum cookie é criado. Preencha com o ID do GA4
(formato `G-XXXXXXXXXX`) para ligar a medição.

Independente disso, os eventos já são empilhados em `window.dataLayer`, de onde um Google Tag
Manager futuro pode lê-los. Eventos disparados:

| Evento | Quando |
|---|---|
| `page_context` | Em toda visita, com a seção (home / tese / blog / institucional) |
| `whatsapp_click` | Clique em qualquer CTA de WhatsApp, identificando de onde partiu |
| `form_start` | Primeiro campo do formulário recebe foco |
| `form_submit` | Envio do formulário, com a área de interesse escolhida |
| `telefone_click` / `email_click` | Clique em `tel:` ou `mailto:` |
| `scroll_depth` | 25%, 50%, 75% e 100% da página — mede se as páginas são lidas |

O arquivo respeita o sinal *Do Not Track* do navegador antes de carregar qualquer script externo.

## Formulários

Os dois formulários (`index.html` e `diagnostico.html`) usam **FormSubmit**, que entrega o conteúdo
por e-mail. Campos de controle já configurados: `_next` (redireciona para `obrigado.html` após o
envio), `_captcha=false`, `_template=table` e `_honey` (armadilha anti-spam). Há caixa de
consentimento obrigatória apontando para a Política de Privacidade.

> O primeiro envio a partir de um endereço de destino novo exige que a FormSubmit confirme o e-mail.
> Se os formulários pararem de entregar, é o primeiro lugar a checar.

## Pendências

1. **E-mail de contato da própria marca.** O endereço exibido no rodapé, na política de privacidade
   e usado como destino dos formulários ainda é o de outra marca. Criar um endereço no domínio
   `exitoadvogados.com.br`, confirmá-lo na FormSubmit e só então trocar em todas as páginas.
2. **51 artigos antigos do blog repetem o mesmo texto.** Os corpos são de 97,8% a 99,8% idênticos
   entre si. Estão `noindex`, fora do sitemap e fora da listagem do blog; continuam linkados apenas
   pelas teses antigas. Devem ser substituídos por artigos reais, tema a tema, e então removidos.
3. **As 17 teses antigas** (as páginas de serviço feitas antes do sistema de conteúdo) repetem as
   mesmas 3 perguntas frequentes e parte do texto. O caminho é reescrevê-las como arquivos em
   `conteudo/servicos/`, uma a uma.
4. **Confirmar a razão social** exibida no rodapé, na Política de Privacidade e nos Termos, e
   incluir o número de inscrição da sociedade na OAB.
5. **Página "Sobre" e página de contato com mapa** ainda não existem.
6. **Publicidade na advocacia.** Todo texto novo deve seguir o Provimento nº 205/2021 do Conselho
   Federal da OAB: informativo, sem promessa de resultado, sem honorário exposto, sem linguagem
   mercantil.
7. **Revisão jurídica.** Os textos de `conteudo/` foram escritos com base na legislação e na
   jurisprudência vigentes em setembro de 2026 e devem ser revisados por advogado do escritório
   antes da publicação.
