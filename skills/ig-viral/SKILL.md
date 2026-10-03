---
name: ig-viral
description: >-
  Vai atrás dos Reels que estão funcionando de verdade agora no nicho do
  usuário, ranqueia pelo quanto cada um superou a própria conta, dá nome à
  fórmula de gancho de cada um e transforma isso num swipe file pra gravar.
  Use quando o usuário disser "acha vídeos que viralizaram", "o que tá
  funcionando agora", "o que a galera do meu nicho tá postando", "faz a
  engenharia reversa desse perfil", "monta um swipe file pra mim", "por que
  esse reels bombou", ou perguntar o que fazer em seguida sem ter evidência
  pra responder.
---

# ig-viral

A skill de pesquisa. Todo o resto deste pacote escreve; esta vai olhar. Rode
uma vez por mês, não todo dia. Fórmula dura uma temporada.

Uma ferramenta mora nesta pasta, e ela roda:

```bash
python3 swipe.py coletados.tsv --out ~/.claude/instagram/swipe.md
```

## A ideia que faz isso valer a pena

**View bruta não é evidência.** Uma conta com dois milhões de seguidores
fazendo 400 mil views teve uma terça fraca. Uma conta com quatro mil
seguidores fazendo 400 mil views achou alguma coisa, e essa coisa dá pra
copiar.

Então tudo aqui é ranqueado pelo **múltiplo**: views divididas pela mediana
recente da própria conta. Acima de 3x é sinal. Abaixo de 1,5x é o dia normal
daquela conta e não ensina nada, por maior que o número pareça.

Colete contas **até umas 10x o tamanho do usuário**. Uma fórmula que funciona
com 2 milhões de seguidores muitas vezes funciona porque a conta tem 2
milhões de seguidores.

## Passo 1: escolha as contas

Peça ao usuário de 6 a 12 contas, ou proponha e peça aprovação:

- **4 diretas**: mesmo nicho, mesma oferta, um pouco à frente.
- **4 vizinhas**: outro nicho, mesmo público. É daqui que os formatos são
  emprestados antes de alguém do nicho ter.
- **2 a 4 gigantes**: contas muito maiores, só pelo formato, nunca pela
  frequência ou pelo tom.

Peça também pra ele abrir os **itens salvos** dele. É o acervo mais rápido e
mais relevante que existe, e já vem filtrado pelo gosto dele.

## Passo 2: vá olhar

Use a ferramenta de navegação que esta sessão tiver de verdade: um navegador
dentro do app, uma extensão ligada ao Chrome do próprio usuário, ou uma
ferramenta de uso do computador. Não existe API pra isso e não precisa,
porque o volume é pequeno o bastante pra ler.

**Regras que não se negociam:**

- **Nunca entre no Instagram em nome do usuário e nunca peça senha.** Se a
  página pede login, quem já está logado é o usuário. Use o navegador dele
  com ele presente, ou peça pra ele colar.
- **Isto é leitura, não raspagem.** Dez contas, uma dúzia de Reels cada, em
  velocidade de gente. Coleta automatizada em volume viola os Termos de Uso
  do Instagram e faz contas levarem bloqueio de ação. Não monte um crawler,
  não use serviço de scraping e não deixe isso rodando em segundo plano.
- **Copie a fórmula, nunca o vídeo.** O formato do gancho, a estrutura, a
  duração, o padrão de cortes. Não o roteiro, não a voz, não a edição da
  pessoa. Credite cada linha do swipe file à conta de onde ela veio.

**O que anotar de cada Reels**, nas palavras do próprio criador:

| campo | observação |
| --- | --- |
| conta | o @ |
| seguidores | do perfil |
| mediana | olhe os últimos 12 Reels e pegue a contagem de views do meio |
| views | deste Reels |
| gancho | a primeira frase, falada ou na tela, literal, com erro de português e tudo |
| na tela | a primeira cartela de texto, se for diferente |
| duração | em segundos |
| cta | o que a pessoa pediu no final |

A mediana é a que importa. Sem ela você volta a ranquear por número de
seguidores, que é exatamente o que esta skill existe pra impedir.

**Quando o Instagram não mostra o suficiente:** a mesma gramática de gancho
roda no YouTube Shorts, onde contagem de views e legendas automáticas são
públicas e não precisa de login. É um segundo acervo legítimo, e o gancho
falado é mais fácil de pegar:

```bash
# contagem de views dos Shorts de um canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# a primeira frase falada de um Short, pela legenda automática em português
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "pt.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DO_VIDEO"
```

Pegue toda palavra da legenda com marcação de tempo abaixo de 3,0 segundos.
Esse é o gancho como foi dito, não como foi escrito. Legenda automática erra
nome próprio e número com frequência; confira esses no áudio.

## Passo 3: ranqueie

Preencha um arquivo separado por tabulação com uma linha de cabeçalho e rode o
script. O cabeçalho pode ser em português ou em inglês, e os números podem vir
como "412.000", "412 mil", "48k" ou "1,2 mi":

```
conta	seguidores	mediana	views	gancho
@alguem	48 mil	11 mil	412.000	ninguém te conta que os seus primeiros 30 reels são pra flopar mesmo
```

```bash
python3 swipe.py coletados.tsv --out ~/.claude/instagram/swipe.md
```

Ele calcula o múltiplo, dá nome à fórmula do gancho usando as mesmas 26
fórmulas com que o `/ig-reel` escreve, dá nota a cada gancho com o
`hookscore.py` e mostra o que separa o terço de cima do terço de baixo.

As expressões que reconhecem as fórmulas foram escritas pra fala brasileira,
mas ainda não foram medidas contra ganchos brasileiros reais. A versão em
inglês nomeava 49% dos ganchos reais; espere algo nessa faixa ou menos, e
leia os "sem classificação" na mão.

## Passo 4: diga o que isso significa, com cuidado

Relate três coisas e nada mais:

1. **Quais fórmulas aparecem demais** no terço de cima, com contagem. Duas
   fórmulas aparecendo quatro vezes cada em seis contas é um achado. Uma
   aparecendo duas vezes não é.
2. **O que o terço de cima tem em comum na estrutura** que o terço de baixo
   não tem: tamanho do gancho, se a entrega é visual, se o primeiro quadro tem
   movimento, onde fica o pedido.
3. **As linhas sem classificação.** Todo gancho que o classificador não
   conseguiu nomear é ruído ou uma fórmula que ainda não está no
   `hooks.json`. Leia na mão. É a coluna mais valiosa da saída, e é por isso
   que o script imprime a contagem.

Depois diga o tamanho da amostra e o grau de confiança em palavras simples.
Quarenta Reels em seis contas sustentam uma afirmação. Doze não, e dizer isso
é a diferença entre pesquisa e horóscopo.

## Passo 5: transforme em algo pra gravar

Pras três fórmulas de cima, escreva **a versão do usuário**: a história dele,
o número dele, no formato que está funcionando. Passe cada uma pro `/ig-reel`
com o número da fórmula já escolhido.

Nunca devolva "faz um reels igual a esse". Devolva uma frase de gancho que ele
poderia falar amanhã.

## Saída

As linhas dos Reels abaixo são saída real do `swipe.py`; o resto é o
relatório que você escreve em cima dela.

```
SWIPE  ·  38 reels  ·  7 contas  ·  base: mediana da conta

FORA DA CURVA (acima de 3x)
  38,5x  gancho 79  #3  Ninguém Te Conta     @conta_a   412.000  (mediana 10.700)
  11,2x  gancho 51  #9  Rouba Isso           @conta_c   180.000  (mediana 16.100)
   7,5x  gancho 51  #2  Pare de Fazer Isso   @conta_d    71.000  (mediana 9.400)
  ...

O QUE ESTÁ APARECENDO DEMAIS
  #3 Ninguém Te Conta   x5 no terço de cima, 0 no de baixo
  #2 Pare de Fazer Isso x4
  tamanho do gancho     8 palavras em cima, 19 embaixo

SEM CLASSIFICAÇÃO (6)
  Dois desses têm o mesmo formato e ele não está no hooks.json: um gancho
  que abre lendo em voz alta o comentário de outra pessoa. Vale acrescentar.

A SUA VERSÃO
  #3  "Ninguém te conta que as suas primeiras 20 propostas são pra perder."
  ...
```

Grave o swipe file em `~/.claude/instagram/swipe.md`. O `/ig-reel` e o
`/ig-plan` leem esse arquivo, e é esse o ponto: depois que isto roda uma vez,
o resto do pacote trabalha com a evidência do próprio usuário em vez de
trabalhar com padrões.

Esta skill não posta, não segue, não curte e não manda mensagem. Ela lê.
