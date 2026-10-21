# Site público da OLIMAIS

Site de uma página (mais Política de Privacidade e página 404), feito em HTML e CSS puros.
Não precisa instalar nada, não tem painel e não depende de nenhum serviço externo: a fonte
(Poppins), os ícones e as imagens ficam dentro da própria pasta. Para ver como está, é só
abrir o `index.html` com dois cliques.

O portal (`portal.olimais.com.br`) é outro projeto e **continua exatamente como está**. O
site só tem botões "Acessar portal" que levam até ele.

---

## 1. Antes de publicar: confira estes 4 pontos

*Já conferido: o CNPJ (67.935.598/0001-81), o Instagram (`@olimaisoficial`), o LinkedIn
(`linkedin.com/company/olimais`) e as fotos (versões em alta qualidade, otimizadas para o site).*

1. **Formulário de professores.** Os dois botões "Quero dar aulas" da página de professores (o do topo e o da caixa
   "Quer fazer parte da OLIMAIS?", no fim da página) abrem o Google Forms da OLIMAIS. Para trocar o formulário um dia,
   procure `docs.google.com/forms` no `professores.html` (são 2 ocorrências) e troque nas duas. O WhatsApp continua só
   nos botões "Fale conosco" e nos ícones do cabeçalho e do rodapé.
2. **Depoimentos reais.** Os 7 depoimentos da seção "O que as famílias dizem" são relatos reais enviados pela
   OLIMAIS. Confirme que cada pessoa autorizou a publicação (e, no caso de alunos menores de idade, que o responsável
   autorizou). Por privacidade, o site mostra só o primeiro nome e o papel (mãe, pai, aluno), sem nomes de filhos nem de
   escolas. Guarde a autorização por escrito (uma mensagem de WhatsApp serve).
3. **Disciplinas, níveis de ensino e preços não aparecem**, porque não tinha essa
   informação. Dá para acrescentar uma seção depois.
4. **Política de privacidade e termos.** A Política de Privacidade, os Termos de Uso e os Termos de
   Aulas (este último com o texto enviado pela OLIMAIS, sem alterações) são modelos base: a política e os
   termos de uso foram escritos para o que o negócio faz hoje (site sem cookies, atendimento por WhatsApp,
   portal e avisos automáticos de confirmação). Vale a revisão de um(a) advogado(a) de direito do consumidor/digital. Se um dia instalar Google Analytics, pixel de anúncios
   ou um formulário próprio no site, o texto precisa ser atualizado. O texto já prevê o link para o
   formulário externo de professores; confirme se ele corresponde ao que o formulário realmente pede.

---

## 2. O que tem dentro

```
index.html          a página principal (os textos dela estão aqui)
professores.html    a página "Para professores" (separada da principal)
privacidade.html    Política de Privacidade
termos-de-uso.html  Termos de Uso do site
termos-de-aula.html Termos de Aulas (regras de agendamento, pagamento e cancelamento)
404.html            página de "não encontrada"
css/style.css       cores, fonte e tamanhos (as variáveis estão no topo do arquivo)
js/main.js          menu do celular e carrossel de depoimentos
img/                fotos, quadrinhos do Instagram, imagem de compartilhamento, ícones
fonts/              Poppins (a fonte dos seus posts) + licença OFL.txt
favicon.svg         ícone da aba do navegador
robots.txt, sitemap.xml   para o Google
.nojekyll           avisa o GitHub que não há Jekyll aqui (opcional)
```

**Ficam só no repositório do GitHub (não vêm neste pacote, e não devem ser apagados nem reenviados):**

```
.github/workflows/instagram.yml   a automação que busca os posts do Instagram a cada 6 horas
scripts/instagram_sync.py         o programa que essa automação roda
data/instagram.json               a lista dos posts mais recentes (a automação reescreve sozinha)
img/instagram/                    as imagens desses posts (a automação reescreve sozinha)
```

### Instagram automático

A seção "Acompanhe a OLIMAIS no Instagram" mostra os 4 posts mais recentes: o `js/main.js` lê o
`data/instagram.json` (atributo `data-insta-feed` no `index.html`) e troca os 4 quadrinhos fixos
(`img/insta-*.jpg`) pelos posts. Se o arquivo faltar ou falhar, os quadrinhos fixos continuam
aparecendo, então eles são a reserva. A chave do Instagram fica **só** no segredo `INSTAGRAM_TOKEN`
do repositório (Settings → Secrets and variables → Actions) e é renovada sozinha toda segunda-feira.
O passo a passo completo está no `GUIA-INSTAGRAM.md`.

Se você enviar um pacote do site, **não envie** as pastas `data/` e `img/instagram/` de outro lugar,
porque elas apagariam os posts já baixados. Este pacote já vem sem elas.

## 3. Como editar

- **Textos:** os da página principal estão no `index.html`; os da página de professores, no
  `professores.html`. Abra no Bloco de Notas (ou em qualquer editor), use "Localizar" para
  achar a frase e troque.
- **Título do topo:** é "Aulas particulares online e presenciais". Procure `titulo-principal` no
  `index.html`.
- **CNPJ:** é `67.935.598/0001-81` (aparece no rodapé de cada página e na política de privacidade;
  procure esse número para trocar).
- **WhatsApp:** procure `5521977003208` (os links) e `(21) 97700-3208` (o texto do rodapé e
  da política de privacidade).
- **Mensagem que já vem escrita no WhatsApp:** é o trecho depois de `?text=` nos links. Para
  mudar, é mais fácil me pedir.
- **Instagram:** procure `olimaisoficial` (aparece no cabeçalho, na seção do Instagram, nos 4
  quadrinhos e no rodapé).
- **LinkedIn:** procure `linkedin.com/company/olimais` (rodapé, página de professores e
  dados do Google).
- **Portal:** procure `portal.olimais.com.br`.
- **Cores:** no topo do `css/style.css`, bloco `:root`. Cada cor tem um comentário dizendo
  onde é usada.
- **Faixa colorida** ("Nossa forma de fazer", na página principal): é uma seção
  `<section class="band band--clay">` (terracota); `band--night` é a versão escura. Para mudar a
  cor, troque uma palavra pela outra. O título
  fica no topo, ao lado do texto, e o tamanho dele segue a regra `h2` do `css/style.css`, para
  ficar proporcional ao texto. Fundos de seção alternam de propósito
  (claro, faixa, claro, areia...) para marcar onde uma seção termina e outra começa.
- **Página de professores:** é curta de propósito: título à esquerda; texto e botões à direita; e
  uma linha com 4 vantagens (a lista `<ul class="points">` no `professores.html`); e, no fim, a
  caixa "Quer fazer parte da OLIMAIS?" com o botão grande para o formulário. Para deixá-la ainda
  mais enxuta, apague a seção `perks` inteira.
- **Barra superior:** é amarela (a cor `--sun`, do bloco `:root` no topo do `css/style.css`). O
  estilo dela está em `.site-header`. A marca do logo, o botão "Fale conosco" e o sublinhado dos
  links ficam pretos justamente para aparecerem sobre o amarelo.
- **Cartões de atalho** (Aulas online, Aulas presenciais, Sobre nós, Depoimentos): a largura de
  cada um está em `.tiles` (o número `212px`) e a altura em `.tile` (`min-height`), no
  `css/style.css`.
- **Banner do topo:** é a foto `img/hero-banner.jpg` (2000×740) com o título e o botão por cima, à
  esquerda, sobre a parede clara. No celular e no tablet o texto vem primeiro e a foto logo abaixo,
  usando o recorte `img/hero-banner-mobile.jpg`. Para trocar a foto, mantenha o lado esquerdo
  limpo (é onde o texto fica) e a proporção de cerca de 2,7 por 1; ou me envie a foto nova que eu
  ajusto os dois arquivos.
- **Trocar uma foto:** substitua o arquivo em `img/` mantendo o nome. As duas fotos da seção
  "Sobre nós" são
  `img/juliana.jpg` (800×1200, proporção 2:3) e `img/juliana-e-alessandra.jpg` (800×1067,
  proporção 3:4); 800 pixels de largura já ficam nítidos até em tela de celular de alta
  resolução. Guarde os originais: no site ficam versões menores, que carregam rápido. Se
  a nova foto tiver outra proporção, ajuste também `width` e `height` do `<img>` no
  `index.html` e o `aspect-ratio` correspondente no `css/style.css`.
- **Quadrinhos do Instagram:** são 4 imagens quadradas (`img/insta-*.jpg`). Troque quando
  postar algo novo que queira mostrar.
- **Depoimentos:** no `index.html`, procure `Depoimentos REAIS`. Cada depoimento é um bloco
  `<figure class="quote">…</figure>`. Para acrescentar um, copie um bloco inteiro e ajuste o
  `aria-label="1 de 7"` de todos. Depoimento comprido leva `class="quote quote--long"` (aparece resumido, com o
  botão "Ler depoimento completo").
- **Domínio principal:** o endereço `https://olimais.com.br/` aparece no `index.html`
  (canonical, prévia de compartilhamento e dados estruturados), no `professores.html`, no
  `privacidade.html`, no `sitemap.xml` e no `robots.txt`. Se decidir usar `www.olimais.com.br` como principal, troque
  nesses lugares.

---

## 4. Como publicar de graça (GitHub Pages)

> **Atenção:** o GitHub Pages gratuito só publica de repositório **público**. Não tem
> problema: tudo que está nesta pasta já é público no site. **Nunca coloque senhas ou dados
> de alunos nesse repositório.** O repositório do portal continua privado e separado.

### Passo 1: criar o repositório
No GitHub: botão **+** → **New repository** → nome `olimais-site` → marque **Public** →
**não** marque "Add a README" → **Create repository**.

### Passo 2: enviar os arquivos
- **Pelo navegador:** na página do repositório vazio, clique em **uploading an existing
  file**, arraste o **conteúdo** da pasta `olimais-site` (os arquivos e as pastas, não a
  pasta em si) e clique em **Commit changes**. Se o `.nojekyll` (arquivo oculto) não subir,
  não tem problema.
- **Pelo git (como no portal):**
  ```
  cd olimais-site
  git init
  git add .
  git commit -m "site inicial"
  git branch -M main
  git remote add origin https://github.com/SEU-USUARIO/olimais-site.git
  git push -u origin main
  ```

### Passo 3: ligar o GitHub Pages
No repositório: **Settings** → **Pages** → em "Source" escolha **Deploy from a branch** →
Branch **main** e pasta **/(root)** → **Save**. Em 1 a 3 minutos aparece o endereço
`https://SEU-USUARIO.github.io/olimais-site/`. **Abra e teste tudo ali** (menu, botões,
carrossel, política de privacidade) antes de ligar o domínio.

### Passo 4: verificar o domínio (recomendado)
A documentação do GitHub recomenda verificar o domínio antes de usá-lo, para ninguém mais
conseguir publicar um site no seu domínio.
1. Clique na sua foto (canto superior direito) → **Settings** (do seu perfil, não do
   repositório) → **Pages** → **Add a domain** → digite `olimais.com.br`.
2. O GitHub mostra um registro **TXT**. No Registro.br (zona de DNS, Modo Avançado, **Nova
   entrada**), crie esse TXT com o **nome** e o **valor** exatamente como o GitHub mostrar. O
   nome tem a forma `_github-pages-challenge-SEU-USUARIO`.
3. Espere o DNS atualizar (pode ser imediato ou levar até 24 horas), volte na mesma tela do
   GitHub e clique em **Verify**. **Mantenha o TXT para sempre** no DNS.

### Passo 5: colocar o domínio no repositório
Repositório → **Settings** → **Pages** → **Custom domain** → `olimais.com.br` → **Save**. O
GitHub cria sozinho um arquivo `CNAME` no repositório (não crie à mão).

> A ordem importa: segundo o GitHub, adicione o domínio aqui **antes** de mexer no DNS dos
> registros A/CNAME, para evitar que alguém use um subdomínio seu.

### Passo 6: apontar o domínio no Registro.br
Em **Registro.br → seu domínio → editar zona DNS → Modo Avançado → Nova entrada**, crie:

| Tipo  | Nome            | Dados                  |
|-------|-----------------|------------------------|
| A     | em branco (o próprio `olimais.com.br`) | `185.199.108.153` |
| A     | em branco       | `185.199.109.153`      |
| A     | em branco       | `185.199.110.153`      |
| A     | em branco       | `185.199.111.153`      |
| CNAME | `www`           | `SEU-USUARIO.github.io` |

(Os endereços acima são os oficiais do GitHub Pages, conferidos na documentação em outubro
de 2026. No CNAME, use só `SEU-USUARIO.github.io`, **sem** o nome do repositório.)

Opcional, para IPv6: mais 4 registros do tipo **AAAA**, também com nome em branco:
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153` e `2606:50c0:8003::153`.
O GitHub recomenda manter os registros A mesmo usando os AAAA.

**Cuidados importantes**
- **Não apague nem altere** os registros que já existem: o `CNAME portal` e o TXT do portal, os
  `MX` e os `TXT` do Google (e-mail). O site novo mexe só no domínio raiz e no `www`.
- Se já existir algum registro **A, AAAA ou CNAME** para o próprio `olimais.com.br` ou para o
  `www` (por exemplo, um padrão do Registro.br), apague **só esses** antes de criar os novos.
- Se o painel não aceitar o nome em branco, me mande um print e eu ajusto este passo.
- Não use registros "curinga" (`*`), por segurança.

### Passo 7: HTTPS e conferência
Em até 24 horas, em **Settings → Pages**, a opção **Enforce HTTPS** fica disponível: marque.
Depois confira:
- `https://olimais.com.br` abre o site (e `https://www.olimais.com.br` redireciona para ele);
- `https://olimais.com.br/professores.html` abre a página "Para professores";
- `https://portal.olimais.com.br` continua funcionando;
- o e-mail do domínio continua funcionando (mande um e-mail de teste).

### Se algo não funcionar
- **"Enforce HTTPS" cinza:** o DNS ainda não propagou. Espere (até 24 h) e confira os 4
  registros A.
- **Aviso de domínio no Pages:** confira se não sobrou registro antigo para `olimais.com.br`
  ou `www`.
- **O `www` não redireciona:** confira se o CNAME aponta para `SEU-USUARIO.github.io` (sem o
  nome do repositório).
- **A página abre sem estilo no endereço `github.io/olimais-site/`:** só a página 404 usa
  caminhos absolutos e isso é esperado nela; o `index.html` funciona normalmente.

---

## 5. Depois que estiver no ar

- Coloque o endereço do site na bio do Instagram e no WhatsApp.
- Vale criar o perfil da empresa no Google (Google Meu Negócio / Business Profile), indicando
  que o atendimento presencial é no Rio de Janeiro, e cadastrar o site no Google Search
  Console (o `sitemap.xml` já está pronto).
- Me peça para ajustar o **portal**: um link "Voltar ao site" na tela de login e um `noindex`
  para o Google não listar as telas de login.

---

## 6. Créditos e licenças

- **Fonte Poppins:** licença SIL Open Font License 1.1 (texto em `fonts/OFL.txt`). Os arquivos
  foram reduzidos aos caracteres usados em português.
- **Ícones:** desenhados no estilo da biblioteca Feather (licença MIT). O ícone do WhatsApp
  e o do LinkedIn vêm do conjunto Simple Icons (domínio público, CC0); as marcas WhatsApp e
  LinkedIn pertencem a seus donos (Meta e LinkedIn).
- **Logo, textos e fotos:** são da OLIMAIS.
