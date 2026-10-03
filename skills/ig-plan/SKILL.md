---
name: ig-plan
description: >-
  Monta a semana no Instagram - o que postar, em qual formato, em que horário
  e com quem interagir. Use quando o usuário disser "planeja minha semana",
  "o que eu posto essa semana", "calendário de conteúdo", "cronograma de
  posts", "tô sem ideia do que postar", "não sei o que postar", ou quiser
  horários de postagem e uma lista de engajamento.
---

# ig-plan

A sala de controle. Todo o resto deste pacote executa; esta skill decide o que
vai ser executado. Rode uma vez por semana, sempre no mesmo dia.

## Entrada

Se `~/.claude/instagram/voice.md`, `swipe.md` e `log.md` existirem, leia os
três. O swipe file é a evidência do próprio usuário, tirada do `/ig-viral`,
sobre quais fórmulas estão funcionando no nicho dele agora, e ela vale mais do
que qualquer coisa escrita neste arquivo. O log impede o plano de repetir um
tema das últimas duas semanas.

Se não existirem, peça quatro coisas e anote:

1. O que o usuário vende, e pra quem.
2. Os três ou quatro temas pelos quais ele quer ser conhecido.
3. O que aconteceu de verdade nesta semana: uma call com cliente, um número,
   um erro, uma coisa que ele construiu, uma discussão que teve. É daí que os
   posts saem.
4. Dez contas pras quais vale a pena ser visto.

## O que postar

Quatro a cinco posts por semana, e pelo menos três deles Reels. Reels é o único
formato do Instagram que chega com regularidade em quem não segue a conta.
Carrossel aprofunda com quem já segue. Stories são diários e são planejados à
parte.

Misture ao longo da semana, nunca dois do mesmo tipo seguidos:

| tipo | frequência | função |
| --- | --- | --- |
| **Prova** | 1 por semana | algo que aconteceu, com um número. Reels. |
| **Ensino** | 1 a 2 por semana | uma coisa que quem assiste pode fazer hoje. Reels ou carrossel. |
| **Opinião** | 1 por semana | uma posição que pode te custar seguidores. Reels. |
| **História** | 1 a cada duas semanas | uma cena com um custo. Reels. |
| **Oferta** | 1 a cada duas semanas | o que você vende, dito com todas as letras, sem pedir desculpa. Carrossel ou stories. |

Pra cada espaço, informe: o tema, o ângulo específico tirado do que aconteceu
nesta semana, o formato e o número da fórmula de gancho do
`ig-reel/hooks.json`. Não é um assunto, é um ângulo. "IA" não é plano. "A
proposta que a gente perdeu porque o rascunho tinha um travessão" é um Reels.

## Quando postar

Poste quando o público está acordado e fora do trabalho. Pra maioria dos
públicos de consumo isso é o começo da noite no horário local; pra público de
negócios, cedo de manhã.

Mas diga isto com todas as letras: **o horário importa muito menos do que os
dois primeiros segundos.** O Instagram continua mostrando um Reels por dias se
ele performa, e enterra um que foi postado na hora certa e não performa. Se o
usuário está otimizando horário de postagem antes de os ganchos funcionarem,
ele está polindo a coisa errada, e você deve dizer isso.

Escreva os horários no horário de Brasília, que é o fuso da maior parte do
público brasileiro, e diga isso no plano. Ancore os horários no fuso do
público, não no do usuário, se forem diferentes: quem mora em Manaus ou em
Cuiabá e fala com o Brasil inteiro posta pelo horário de Brasília, e quem mora
em Lisboa e fala com brasileiros também.

## A rodada de engajamento, que não é opcional

20 minutos por dia, antes de postar, não depois. Monte uma lista de 10:

- **5 de alcance** - contas com o público que o usuário quer, onde um bom
  comentário é visto. Comente cedo, antes de a conversa ter 200 comentários.
- **3 pares** - mesmo tamanho, mesma área. É o grupo que retribui.
- **2 compradores** - gente que poderia comprar de verdade. Comente por semanas
  antes de qualquer DM, e nunca venda num comentário.

Passe a lista pro `/ig-comment`.

## Saída

```
SEMANA DE 15/09  (horário de Brasília)

SEG  só engajamento  (20 min, lista abaixo)
TER  19h30  REELS      PROVA     #5  Horas Viram Minutos - proposta de 5 horas em 20 min
QUA  só stories + engajamento
QUI  19h00  CARROSSEL  ENSINO    legenda Trabalho B      - a cláusula destrinchada em 4 slides
SEX  19h30  REELS      OPINIÃO   #2  Pare de Fazer Isso  - pare de fazer call de diagnóstico
SÁB  -
DOM  18h00  REELS      HISTÓRIA  #21 Começo no Meio      - o e-mail pedindo reembolso

STORIES  todo dia, 3 a 5 quadros, caixa de perguntas na quinta.

ENGAJAMENTO  (5 de alcance / 3 pares / 2 compradores)
  ...

Diz "escreve o de terça" que eu faço o rascunho.
```

Escreva o plano em `~/.claude/instagram/plan.md` pras outras skills lerem.
Nada é agendado nem postado em lugar nenhum. Isto é um plano, e quem executa é
o usuário.
