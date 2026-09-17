# Tocador

Player de áudio local que funciona abrindo o `index.html` direto do disco, sem servidor.

## Por que as músicas não tocavam

O código antigo lia as playlists com `fetch('playlists/manifest.json')`. Em `file://`, Chrome e Firefox
tratam cada arquivo local como uma origem diferente, então qualquer `fetch`/`XHR` é barrado — é exatamente
o erro de CORS que apareceu. O JSON estar válido não muda nada: o navegador nem chega a lê-lo.

Tags como `<script>` e `<audio>` **não** passam por essa checagem. Por isso o tocador agora recebe a lista
de faixas por um `data.js` (um `<script>`) e toca os arquivos por caminho relativo.

## Como usar

Coloque `index.html` e `gerar-dados.py` na raiz do projeto, com a pasta `playlists` do lado:

```
ipod-player/
  index.html
  gerar-dados.py
  playlists/
    Comptia Security + AI podcast/
      Section 01_ Introduction.mp3
      ...
```

Abra o terminal nessa pasta e rode:

```
python gerar-dados.py
```

Isso cria o `data.js`. Agora é só dar dois cliques no `index.html`. Rode o script de novo sempre que
adicionar ou remover áudios.

Sem Python à mão? Clique em **Abrir pasta** no canto superior direito e escolha a pasta `playlists`.
Funciona na hora, mas vale só para aquela sessão. Arrastar arquivos para a janela também funciona.

O `manifest.json` continua sendo lido se você servir a pasta por HTTP (`python -m http.server`), mas
nesse caso o `data.js` nem é necessário.

## O que o tocador faz

- Guarda onde você parou em cada faixa e retoma dali na próxima vez. A barrinha embaixo de cada linha
  mostra o quanto já foi ouvido; faixas concluídas ganham um ✓.
- Velocidade de 1× a 2× no botão ao lado dos controles.
- Volta 15 s / avança 30 s, e passa sozinho para a faixa seguinte no fim.
- Várias playlists: cada subpasta de `playlists` vira uma, selecionável no topo.

### Teclado

| Tecla | Ação |
| --- | --- |
| Espaço | tocar / pausar |
| ← / → | 15 s atrás / 30 s à frente (com Shift, 60 s) |
| J / K | próxima / anterior |

## Formatos

`.mp3`, `.m4a`, `.ogg`, `.wav`, `.flac`, `.aac`, `.opus`, `.webm` — o que o navegador souber tocar.

## Publicando no GitHub Pages

Funciona sim — e lá o problema de CORS nem existe, porque o site passa a ser servido por HTTPS.
Três pontos que costumam derrubar esse tipo de projeto no Pages:

1. **O `data.js` precisa existir no site publicado.** Ou você roda `python gerar-dados.py` antes de
   commitar, ou deixa o workflow em `.github/workflows/deploy.yml` (incluído aqui) gerar na hora do
   deploy. Com o workflow, basta jogar os MP3 na pasta `playlists` e dar push.
2. **Não use Git LFS para os áudios.** O GitHub Pages não serve arquivos em LFS — eles voltam como um
   ponteiro de texto e o player não toca nada. Commit normal mesmo.
3. **Nomes de arquivo diferenciam maiúsculas de minúsculas** no servidor, ao contrário do Windows.
   Como o `data.js` é gerado lendo a pasta de verdade, isso se resolve sozinho — só não renomeie os
   arquivos depois de gerar.

### Passo a passo

1. Crie o repositório e mande `index.html`, `gerar-dados.py`, a pasta `playlists` e o arquivo
   `.nojekyll` (vazio, evita que o Jekyll ignore pastas).
2. Coloque o `deploy.yml` em `.github/workflows/deploy.yml`.
3. No repositório: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Dê push. O endereço sai em `https://SEU-USUARIO.github.io/NOME-DO-REPO/`.

### Limites

Repositório até 1 GB e 100 MB por arquivo, com 100 GB de banda por mês — suas 9 seções somam cerca de
46 MB, então há folga. Se a coleção crescer muito, vale hospedar os áudios fora e apontar o `src` do
`data.js` para lá.

Uma vez publicado, o tocador também aparece nos controles da tela de bloqueio do celular, com título
da faixa, play/pause e pular seção.
