---
name: ig-caption
description: >-
  Escreve a legenda do Instagram: a linha que sobrevive ao corte do "... mais",
  o corpo, o pedido único, os termos de busca e as três hashtags, e revisa tudo
  antes de postar. Use quando o usuário disser "escreve a legenda", "faz a
  legenda desse reels", "o que eu coloco na legenda", "o que eu escrevo na
  descrição", "quais hashtags eu uso", "é publi, como eu sinalizo", ou tiver um
  Reels ou um carrossel pronto e precisar do texto.
---

# ig-caption

Tem uma ferramenta nesta pasta, e ela roda:

```bash
python3 caption.py legenda.txt
python3 caption.py legenda.txt --keywords "contrato de prestação de serviço,precificação"
python3 caption.py legenda.txt --publi
```

Ela imprime a legenda do jeito que o feed imprime: os primeiros 125 caracteres
numa caixa, todo o resto escondido atrás do toque. Leia essa caixa antes de ler
qualquer outra coisa que você escreveu.

## Primeiro, decida qual é o trabalho dessa legenda

É essa decisão que estraga a legenda quando alguém pula ela.

**Trabalho A: o vídeo já fisgou.** Um Reels carrega o próprio gancho nos dois
primeiros segundos, falado e na tela. A legenda não é um segundo gancho, e
competir com o vídeo é o jeito de perder os dois. O trabalho dela é o pedido, o
contexto que faz o pedido fazer sentido e as palavras que as pessoas buscam.

**Trabalho B: a legenda é o conteúdo.** Uma foto, uma imagem só, uma capa de
carrossel que abre um suspense. Aqui a linha um é o gancho e funciona igualzinho
ao gancho de um Reels: concreta, curta, e cortada num suspense, não no meio da
frase.

Pergunte qual dos dois você está escrevendo. Se o usuário tem um Reels com
gancho forte, escreva A e diga por quê.

## O formato

```
Linha 1     125 caracteres de espaço visível. Trabalho A: o pedido, sem
            rodeio. Trabalho B: o gancho.
            Nunca um cumprimento ("oi, gente", "bom dia, família"), nunca
            hashtag, nunca emoji como primeiro caractere.
Corpo       parágrafos curtos, uma linha em branco entre eles. De dois a seis.
            É aqui que moram os termos de busca.
O pedido    um só. Comentar uma palavra-chave, salvar ou chamar na DM. Um.
Hashtags    até cinco, numa linha só delas no final, ou nenhuma.
```

O limite é 2.200 caracteres e quase nada precisa de 2.200. Uma legenda que
ganha o toque e depois entrega 600 caracteres ganha de uma que entrega 1.800.

## Hashtags, sem enrolação

Hashtag não é mais alavanca de alcance, e a plataforma agora disse isso com uma
mudança de produto. **O Instagram limitou as hashtags a cinco por post em 18 de
dezembro de 2025**, contra trinta antes, dizendo aos criadores que usar "menos
hashtags (até 5) e mais específicas, em vez de muitas genéricas" funciona melhor
(tradução livre). O Adam Mosseri já tinha dito em fevereiro de 2025 que hashtag
não aumenta alcance e é uma etiqueta, não uma alavanca de distribuição.

Então: até cinco, específicas, como etiqueta de assunto. Se o usuário tem vinte
hashtags salvas nas notas do celular, prontas pra colar, esse pacote agora é
peso morto e o revisor dá FALHA nele.

`#viral`, `#fyp`, `#explorepage`, `#foryou`, `#sigoevolto`, `#instabrasil` não
descrevem nada. Corte.

## Termo de busca importa mais que hashtag agora

A busca do Instagram lê o texto da legenda. Então a frase pela qual o usuário
quer ser encontrado vai na legenda do jeito que uma pessoa digitaria, numa frase
que se lê normalmente. "Contrato de prestação de serviço" escrito no quarto
parágrafo, e não "#contratodeprestacaodeservico" num bloco no fim.

Peça dois ou três desses termos e passe pro revisor:

```bash
python3 caption.py rascunho.txt --keywords "contrato de prestação de serviço,precificação"
```

Uma legenda de Trabalho A, de uma designer freela, pra um Reels que já abre com
o gancho:

```
Comenta CONTRATO que eu te mando a cláusula que me fez parar de devolver dinheiro pra cliente.

Em 2024 eu devolvi R$ 4.200 pra uma cliente que aprovou a identidade visual inteira e pediu o dinheiro de volta nove dias depois.

A cláusula é uma linha só: pagamento na entrega, não na aprovação. Aprovação é sentimento. Entrega tem data.

Se você é freela e fecha contrato de prestação de serviço pelo WhatsApp, ela vale pra você também.

E muda a conversa de precificação inteira, porque o cliente para de tratar o seu prazo como opcional.

#designgrafico #freeladesign #identidadevisual
```

E o que o revisor devolve:

```
LEGENDA  ·  586 / 2200 caracteres  ·  3 hashtags  ·  1 pedido(s)
================================================================

  O QUE O FEED MOSTRA
  +------------------------------------------------------+
  | Comenta CONTRATO que eu te mando a cláusula que me   |
  | fez parar de devolver dinheiro pra cliente.          |
  |                                                      |
  | Em 2024 eu devolvi R$ 4.200 p                        |
  +-------------------------------------------- ... mais +

  OK    TAMANHO          586 / 2200 caracteres
  OK    PRIMEIRA LINHA   94 caracteres, aparece inteira
  OK    GANCHO CONCRETO  3 número(s) ou nome(s) na janela visível
  OK    HASHTAGS         3 tag(s): #designgrafico #freeladesign #identidadevisual
  OK    LUGAR DAS TAGS   as tags estão depois do corte
  OK    LINKS            nenhum link morto no texto
  OK    UM PEDIDO        uma chamada pra ação: comentar uma palavra-chave
  OK    EMOJI            0 emoji, 0,0 por 100 caracteres
  OK    BUSCA            2/2 presentes, 0 na janela visível
----------------------------------------------------------------
  VEREDITO  PRONTA
```

Os termos de busca ficarem fora da janela visível é normal no Trabalho A: a
linha um é do pedido.

## Regras

- **Nada de link na legenda.** Legenda não é clicável. Uma URL no corpo é texto
  morto que diz "eu não uso essa plataforma". Bio ou DM. "Link na bio" é uma
  frase que todo brasileiro já entende.
- **Um pedido.** Dois pedidos é o mesmo que nenhum. O `caption.py` conta.
- **O pedido de palavra-chave precisa de uma palavra que dê pra digitar.** Uma
  palavra, sem espaço, sem emoji, em maiúsculas, e dita em voz alta no vídeo
  também. `Comenta CONTRATO` funciona. `Comenta "o guia do contrato"` não, e o
  revisor nem conta isso como pedido. `EU QUERO` é o clássico brasileiro e passa
  porque todo mundo digita no automático, mas é genérico: se você tem resposta
  automática de DM em mais de um post, use uma palavra que diga de qual post a
  pessoa veio.
- **Escreva o primeiro comentário separado** se tiver link. Diga isso no recibo.
- **Emoji como pontuação, não enfeite.** O revisor sinaliza qualquer coisa acima
  de 4 a cada 100 caracteres.
- **Texto alternativo vale 20 segundos.** Em carrossel e foto, escreva. Leitor
  de tela lê, e o Instagram também.
- **Publi se diz antes do "... mais".** Post pago ou permuta é publicidade. O
  Código do CONAR (art. 28) exige que anúncio seja identificado como anúncio,
  então "publi" ou "publicidade" vai na primeira linha, à vista, e o post usa a
  marcação de parceria paga do Instagram. Um `#publi` escondido no fim não serve
  aqui. Rode com `--publi`: o revisor dá FALHA se a legenda não diz, AVISO se só
  diz depois do corte. Se a legenda já menciona publi, ele faz essa checagem
  sozinho. Não é parecer jurídico.

A mesma legenda de publi em três versões (sem marcação, com `#publi` no fim, e
com `Publi @planilhei:` abrindo a linha um), linha PUBLI de cada rodada:

```bash
python3 caption.py publi.txt --publi
```

```
  FALHA PUBLI            o post é publi, mas a legenda não diz. Escreva "publi" ou "publicidade" na primeira linha e use a marcação de parceria paga do Instagram
  AVISO PUBLI            a marcação de publicidade só aparece depois do "... mais". Publicidade tem que ser identificada com clareza (CONAR, art. 28): suba pra primeira linha
  OK    PUBLI            a marcação de publicidade aparece antes do "... mais"
```

Conte com isso: `Publi @marca:` come uns 15 a 20 caracteres da linha um. No
teste, só colar a marcação na frente de uma linha de 124 caracteres levou ela
pra 142, e o pedido foi cortado no meio (AVISO em PRIMEIRA LINHA). Reescreva a
linha pra caber, não empurre o pedido pra depois do corte.

## O ciclo

1. Decida Trabalho A ou Trabalho B e diga qual.
2. Escreva o rascunho.
3. Rode `/ig-human` nele. Legenda é curta, então clichê grita mais aqui do que
   em qualquer outro lugar do pacote.
4. Rode o `caption.py` com os termos de busca do usuário, e com `--publi` se o
   post é pago ou permuta. Corrija toda FALHA. Decida sobre todo AVISO em voz
   alta, não em silêncio.
5. Imprima o bloco pronto pra copiar e depois o recibo:

```
LEGENDA PRONTA
trabalho:   A - o Reels carrega o gancho
visível:    94 de 125 caracteres usados antes do corte
pedido:     um, comentar CONTRATO
hashtags:   3
busca:      "contrato de prestação de serviço" no 4º parágrafo, "precificação" no 5º
publi:      não
revisor:    PRONTA
```

Nada é postado. O usuário cola.
