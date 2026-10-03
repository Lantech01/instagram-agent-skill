---
name: ig-repurpose
description: >-
  Transforma um conteúdo longo - vídeo do YouTube, episódio de podcast, live,
  newsletter, aula, post de blog ou call com cliente - numa semana de Reels e
  carrosséis. Use quando o usuário disser "reaproveita esse conteúdo",
  "transforma isso em reels", "faz os cortes desse podcast", "tenho um
  vídeo/uma live/uma transcrição", "picota esse conteúdo", ou colar algo longo
  e quiser levar pro Instagram.
---

# ig-repurpose

Um conteúdo longo bom tem de quatro a seis posts dentro. A maioria das pessoas
tira um e joga o resto fora.

## Entrada

Uma transcrição, um artigo, uma newsletter, um roteiro, um resumo de call, uma
live, a gravação de uma aula ou de um curso, um episódio de podcast. Se o
usuário mandar uma URL e esta sessão tiver uma ferramenta de transcrição, use;
se não, peça pra colar. Se a transcrição veio da legenda automática do YouTube,
desconfie de nomes próprios e números: é onde ela mais erra. Leia a coisa
inteira antes de extrair qualquer coisa.

Se a fonte é um vídeo do próprio usuário, peça o arquivo também. Um Reels feito
com a filmagem dele ganha de um feito com as palavras dele lidas de novo.

## Extrair, não resumir

Um resumo de vídeo não é um Reels. Ninguém quer o resumo. Passe pelo conteúdo
e puxe as coisas que param em pé sozinhas:

| o que puxar | o que é |
| --- | --- |
| **Afirmações** | toda frase que começaria uma discussão |
| **Números** | todo valor, custo, duração, porcentagem |
| **Histórias** | todo momento com uma pessoa, uma cena e um custo |
| **Mecanismos** | todo "o jeito que isso funciona de verdade é..." |
| **Erros** | toda admissão de algo que deu errado |
| **Frases** | toda frase que já dá pra citar do jeito que está |

Liste o que achou, com a contagem, antes de escrever qualquer coisa. Se o
conteúdo rende menos de quatro itens, ele é fraco, e quatro posts espremidos
dele vão ser fracos também. Diga isso.

## Depois, escolha o formato de cada extração

Nem tudo é Reels.

- **Afirmação, erro, história** viram Reels. Precisam de voz e de rosto.
- **Mecanismo, lista numerada** viram carrossel. Precisam ser relidos.
- **Uma frase citável** vira um quadro de story, não um post.

## Depois, monte a semana

Cada extração vira um post, e cada post para em pé inteiro sozinho. Quem
assiste não viu a fonte e nunca vai ver. Nunca escreva "como eu falei no meu
último vídeo", nem "corte do episódio 37" no texto da tela. O post é a coisa.

Atribua uma fórmula de gancho do `ig-reel/hooks.json` a cada um e varie. Cinco
posts de uma fonte com o mesmo formato de gancho parecem fábrica de conteúdo,
porque são.

Se a fonte é vídeo do próprio usuário, **use a filmagem de verdade**. O trecho
em que ele disse a coisa, com a reação real, ganha de uma regravação sempre.
Corte na frase, não na respiração. Corte de podcast que começa no "então, como
eu tava falando" é só um pedaço do episódio, não um post: o corte começa na
frase do gancho.

Ordene a semana assim: a afirmação mais forte primeiro, a história no meio da
semana, e o mecanismo por último, quando quem gostou dos anteriores está
esperando por ele.

## Saída

```
FONTE: "Por que a gente matou a call de diagnóstico" (podcast de 42 min, 8.900 palavras)

ACHEI  5 afirmações, 9 números, 3 histórias, 4 mecanismos, 2 erros, 7 frases citáveis

SEMANA
TER  REELS      #2  Pare de Fazer Isso   Pare de fazer call de diagnóstico
                                         usa o trecho de 14:20, ele ri no final
QUA  CARROSSEL  legenda Trabalho B       O formulário de 4 perguntas que substituiu a call
SEX  REELS      #21 Começo no Meio       "...e ele pediu reembolso nove dias depois"
DOM  REELS      #5  Horas Viram Minutos  Seis horas por semana de volta, um link apagado

Diz "escreve o de terça" que eu faço o rascunho.
```

Depois, escreva sob pedido, um de cada vez, cada um passando pelo `/ig-reel` e
pelo `/ig-human`. Não despeje quatro roteiros prontos de uma vez. Vão soar
todos iguais e o usuário não vai gravar nenhum.
