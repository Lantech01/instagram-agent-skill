---
name: ig-reel
description: >-
  Escreve um Reels do Instagram a partir de uma ideia crua: opções de gancho
  tiradas de 26 fórmulas, o roteiro falado, o texto na tela e um roteiro
  cronometrado, na voz do próprio usuário e com nota antes de gravar. Use
  sempre que o usuário quiser um Reels, um roteiro de vídeo curto, um gancho,
  uma locução, "faz um reels sobre X", "me ajuda com o roteiro", "o que eu
  falo nesse vídeo", "tô sem gancho", ou estiver prestes a gravar sem ter a
  primeira frase.
---

# ig-reel

Transforma uma ideia crua num Reels que alguém assiste até o fim.

Duas ferramentas moram nesta pasta, e as duas rodam de verdade. Use as duas.
Não chute a nota do gancho e não adivinhe a duração.

```bash
python3 hookscore.py ganchos.txt            # ranqueia as opções de gancho
python3 hookscore.py --hook "uma frase"     # dá nota a um gancho só
python3 beats.py roteiro.txt --target 30    # roteiro cronometrado antes de gravar
```

## Antes de escrever

1. Leia `~/.claude/instagram/voice.md`, se existir. É o perfil de voz do
   usuário: como ele fala na câmera, o que ele nunca diz, com quem ele está
   falando. Se não existir, peça **três Reels dele**, transcreva ou leia,
   deduza a voz e escreva o arquivo. Roteiro na voz errada não serve, porque
   ele vai ter que falar aquilo em voz alta.
2. Leia o `hooks.json` desta pasta. São 26 fórmulas, cada uma com um modelo,
   um exemplo preenchido, a versão pra tela, pra que serve e como costuma ser
   estragada. Quatro delas estão lá porque apareciam o tempo todo em ganchos
   reais, não pra completar um padrão.
3. Se a ideia estiver rala, não encha linguiça. Faça uma pergunta só, com
   tudo junto: o que aconteceu, com quem, e quanto custou ou rendeu. Um Reels
   precisa de uma coisa específica e verdadeira. Consiga isso antes de
   escrever.
4. Se `~/.claude/instagram/swipe.md` existir, leia. É o `/ig-viral` que
   escreve esse arquivo, e ele é a evidência do próprio usuário sobre quais
   fórmulas estão funcionando no nicho dele agora. Vale mais que os padrões
   deste arquivo.

## O formato

Um Reels é decidido nos dois primeiros segundos e segurado pelos cinco
seguintes.

```
0:00 - 0:02   GANCHO      a afirmação. Frase falada e frase na tela, escritas
                          separadas. Movimento no primeiro quadro, não um rosto
                          parado.
0:02 - 0:07   O RISCO     por que isso importa pra quem está assistindo. Uma frase.
0:07 - ...    O CORPO     uma ideia por batida, e o quadro muda a cada batida.
ÚLTIMOS 3s    A ENTREGA   entregue o que o gancho prometeu, depois o pedido único.
ÚLTIMA FRASE  O LOOP      repita uma palavra do gancho pro replay encaixar.
```

Duração: de 15 a 45 segundos é a faixa que funciona. Reels vai até 3 minutos
e quase ninguém deveria usar isso. Abaixo de 7 segundos a contagem de loops
infla e nada mais melhora.

## O passo a passo

**1. Escolha três ganchos, não um.** Passe a ideia pelo `hooks.json`, escolha
três fórmulas que encaixem de verdade e escreva a frase falada e a frase da
tela de cada uma. Fórmulas diferentes, não três versões da mesma.

**2. Dê nota.** Coloque as três frases faladas num arquivo, uma por linha, e
rode o `hookscore.py`. Mostre o ranking pro usuário. Se o primeiro ficou
abaixo de 50, você ainda não tem o gancho, e nenhuma edição resolve isso.

As listas de palavras do `hookscore.py` são em português, mas os limites dele
vêm da versão original em inglês e ainda não foram medidos contra ganchos
brasileiros reais. Use a nota pra descartar gancho fraco, não pra escolher
entre dois bons.

**3. Escreva o roteiro** em cima do gancho vencedor. Linguagem falada, do
jeito que o usuário fala de verdade. "Pra", "tá", "a gente", se é assim que
ele fala. Frases curtas. Nenhuma frase que ele precise ensaiar.

**4. Cronometre.** Rode `beats.py roteiro.txt --target {duração}`. Corrija
todo aviso: gancho passando de 3 segundos, qualquer batida acima de 4
segundos, uma sequência de batidas sem nada concreto, falta de loop. Rode de
novo até sair limpo. O padrão é 165 palavras por minuto; se o usuário fala
mais devagar ou mais rápido, passe `--ppm` com o ritmo dele.

**5. Humanize.** Passe o roteiro pelo `/ig-human` antes de mostrar. Uma frase
com cara de texto escrito fica óbvia no momento em que alguém fala em voz alta.

**6. Imprima o bloco.** O roteiro num bloco de código, o texto na tela numa
lista separada com os tempos, e depois:

```
REELS PRONTO
gancho:       #1 Confissão de Custo, nota 77,8 FORTE
duração:      20,0s em 8 batidas a 165 ppm
na tela:      5 cartelas
humanizador:  0 marcas removidas, nota humana {{nota}} {{veredito}}
legenda:      rode /ig-caption em seguida

Responda "sim" pra registrar, ou me diga o que mudar.
```

**7. Nunca publique.** Esta skill entrega um roteiro. Quem grava e posta é o
usuário. No "sim", acrescente ao `~/.claude/instagram/log.md` a data, a
fórmula de gancho usada e a primeira frase, pra o `/ig-audit` ter histórico
depois.

## O texto na tela é um roteiro à parte

Escreva separado, sempre. Ele é lido antes de ser ouvido.

- **Seis palavras ou menos por cartela.** Está sendo lido a um braço de
  distância por alguém que ainda não está prestando atenção no áudio.
- **A cartela do gancho aparece no quadro 1**, não depois de um segundo de
  silêncio.
- **Fique dentro da área segura.** Num quadro de 1080x1920, nada acima de
  y=230 ou abaixo de y=1440, e deixe livres os 230 pixels da direita. A
  interface fica por cima de tudo que está fora dessa caixa: a legenda, a
  coluna de botões, a faixa do áudio.
- **Nunca coloque o gancho onde fica a legenda.** É a parte de baixo do
  quadro, e ela fica coberta.
- **Queime legenda no corpo do vídeo.** A maioria das pessoas assiste sem som
  primeiro.
- **Português ocupa mais espaço que inglês.** Se a cartela não cabe, corte
  artigo e preposição antes de diminuir a fonte.

## Regras que fazem diferença

- **Uma ideia por Reels.** Se o roteiro tem duas, são dois Reels. Diga isso.
- **Número em vez de adjetivo.** "R\$ 4.200" ganha de "muito dinheiro". Se o
  usuário não deu um número, peça um em vez de escrever em volta do buraco.
- **Corte a introdução.** Sem "oi, gente", sem "no vídeo de hoje", sem nome,
  sem vinheta de logo. O vídeo começa na frase que você normalmente diria no
  sexto segundo.
- **Mude o quadro a cada batida.** Plano parado por 8 segundos é onde as
  pessoas saem, e o `beats.py` vai apontar isso.
- **Um pedido no final.** Comenta uma palavra-chave, salva, ou segue. Um só.
- **Nunca invente.** Nada de métrica, cliente, faturamento ou resultado
  inventado no nome do usuário, nem como exemplo provisório. Se precisa de um
  número e ele não existe, deixe `{{seu número}}` no roteiro e avise.
- **Não escreva roteiro em cima de áudio em alta que o usuário não pode
  usar.** Se a ideia precisa da voz dele, diga isso.
- **Se for publi ou permuta, o Reels é publicidade.** Diga isso pro usuário:
  a legenda vai precisar da marcação, e o `/ig-caption` confere.

## Exemplo

```
/ig-reel a gente cortou o tempo de proposta de 5 horas pra 20 minutos com um modelo
```

```
GANCHOS  (com nota do hookscore.py)
  77,8  FORTE  #1  Confissão de Custo   "Perdi quatro horas por semana formatando proposta."
                                         na tela: 4 HORAS POR SEMANA
  54,8  OK     #5  Horas Viram Minutos  "Proposta me levava cinco horas. Hoje leva vinte minutos."
                                         na tela: 5 HORAS -> 20 MIN
  36,6  FRACO  #9  Rouba Isso           "Rouba o modelo de proposta que fez isso."
                                         na tela: ROUBA ISSO

Gravando o #1: o custo é seu, cabe numa cartela, e "quatro horas por semana"
volta no fim como loop. O #5 perdeu porque não tem nada em jogo (TENSÃO 20);
o #9 não diz nada checável (CONCRETUDE 15).
```

```
ROTEIRO CRONOMETRADO  ·  55 palavras  ·  ~20,0s a 165 ppm  ·  meta 20s
  0:00,0   2,5s  GANCHO     Perdi quatro horas por semana formatando proposta.
  0:02,5   2,2s             Por dois anos. Umas quatrocentas horas.
  0:04,7   2,9s             Aí eu montei um modelo com quatro blocos.
  0:07,6   1,4s             Escopo, preço e prazo.
  0:09,1   3,3s  MEIO       E o que acontece se o cliente disser não.
  0:12,4   2,5s             Hoje a proposta sai em vinte minutos.
  0:14,9   2,9s             Comenta MODELO que eu te mando o meu.
  0:17,8   2,2s  CTA        Quatro horas por semana de volta.
  - Loop: a última batida repete "horas, quatro, semana" do gancho.
  - Duração dentro da meta (20,0s para 20s).
```

A primeira versão desse roteiro levava 23,6s, com gancho de 3,6s e três
batidas acima de 4s. Foi o `beats.py` que mostrou onde cortar.
