---
name: ig-audit
description: >-
  Autópsia do que o usuário já postou - quais Reels funcionaram de verdade,
  por quê, e o que parar de fazer. Use quando o usuário colar os Insights ou
  posts antigos e perguntar "o que tá funcionando", "por que esse reels
  flopou", "analisa minhas métricas", "lê meus insights", "audita meu
  conteúdo", "por que meu alcance caiu", ou quiser saber do que fazer mais.
---

# ig-audit

A única fonte honesta do que funciona pra uma conta é a própria conta. Toda
regra de todo guia de Instagram, inclusive as deste pacote, é um palpite
inicial. Os últimos 30 posts do usuário são a evidência.

## Entrada

Peça o que o usuário tiver:

- Insights por post: visualizações, alcance, interações, tempo de
  visualização, salvamentos, compartilhamentos, seguidores ganhos e a parcela
  do alcance que veio de quem não segue a conta. Print serve.
- Ou o gráfico de retenção dos melhores e dos piores Reels recentes. Esse print
  sozinho vale mais do que todo o resto junto.
- Ou só os posts e as visualizações de cada um, o que basta pra uma primeira
  passada.

Leia também `~/.claude/instagram/log.md` se existir, porque ele registra qual
fórmula de gancho cada post usou.

## O que medir de verdade

Visualização bruta é o número menos útil da tela, porque é basicamente função
de quantas pessoas já seguem a conta. Calcule estes no lugar e mostre a conta:

| métrica | como | o que te diz |
| --- | --- | --- |
| **Múltiplo sobre a mediana** | visualizações / mediana de visualizações da própria conta | se foi um acerto de verdade ou um dia normal |
| **Alcance em não seguidores** | % do alcance vindo de quem não segue | se o post viajou, ou não |
| **Retenção aos 3s** | quem ainda está lá aos 3s / quem começou a ver | se o gancho funcionou. Essa é a nota real do gancho. |
| **Tempo médio de visualização** | direto dos Insights | se o meio funcionou |
| **Compartilhamentos por alcance** | compartilhamentos / alcance | o sinal mais forte que dá pra conquistar. Mandar pra alguém é a pessoa colocar o nome dela no seu post. |
| **Seguidores por alcance** | seguidores ganhos / alcance | se o perfil converteu a atenção |

Ranqueie por múltiplo e por compartilhamentos por alcance, não por
visualizações. Um Reels com 4.000 visualizações e 90 compartilhamentos ganhou
do de 60.000 visualizações e 11.

A taxa de engajamento que vai pro mídia kit (interações divididas por
seguidores) também fica de fora: ela diz como a base reagiu, não se o post saiu
da base. Aqui tudo é dividido pelo alcance.

## Depois, ache o padrão

Com os cinco melhores e os cinco piores lado a lado, procure o que separa os
dois grupos, e esteja disposto a concluir uma coisa que o usuário não vai
gostar de ouvir:

- **Retenção aos 3 segundos.** Se o topo e o fundo diferem aqui, é o gancho e
  mais nada, e todo o resto é distração.
- **Fórmula de gancho.** Quais ids do `ig-reel/hooks.json` estão nos cinco
  melhores?
- **Formato.** Reels, carrossel, imagem única.
- **Duração.** Agrupe em menos de 15s, 15 a 30s, 30 a 60s, mais de 60s.
- **Tema.**
- **Se o usuário respondeu os comentários na primeira hora.**
- **Dia e horário.** Confira isso **por último** e só se o resto não mostrar
  nada. Quase nunca é a causa, e é onde as pessoas querem que a causa esteja.

Diga a conclusão como uma afirmação com a evidência junto, e diga o quanto
confia nela. Com 30 posts dá pra ver um padrão. Com 6 não dá, e dizer isso é
melhor do que inventar um.

## A distinção que economiza meses

**Um Reels que tem visualização e não traz seguidor não é um Reels que falhou,
é um problema de perfil.** Um Reels que não tem visualização é um problema de
gancho. Separe os dois antes de recomendar qualquer coisa. Se o alcance em não
seguidores é alto e os seguidores por alcance são baixos, pare de reescrever
gancho e vá pro `/ig-profile`.

## Saída

```
AUDITORIA  ·  31 posts  ·  12/06 a 05/09  ·  mediana 4.100 views

5 MELHORES POR MÚLTIPLO
  18,2x  #3  Ninguém Te Conta     74.600 views  62% não seguidores  ret. 3s 71%  128 compart.
   6,4x  #1  Confissão de Custo   26.300 views  48% não seguidores  ret. 3s 64%   71 compart.
  ...

5 PIORES
   0,3x  #11 Lista com Favorito    1.200 views   9% não seguidores  ret. 3s 31%    2 compart.
  ...

O QUE OS DADOS DIZEM
1. A retenção aos 3 segundos é a história inteira. Os cinco melhores têm média
   de 66%, os cinco piores, 33%. Todo o resto que te preocupa vem depois dos
   dois primeiros segundos.
2. Os posts em que quem sai mal na foto é você: média de 8,1x contra 0,9x de
   todo o resto. n=5. É o sinal mais forte daqui, e não é por pouco.
3. Lista de ferramentas dá visualização e mais nada. Alcance alto, nenhum
   compartilhamento, nenhum seguidor. Três dos seus cinco piores.
4. Dia da semana não mostra nada. As médias de terça e de sexta estão dentro do
   ruído. Pare de otimizar isso.

PARE: listas de ferramentas.
FAÇA MAIS: os posts com um custo que você pagou e um número junto.
```

Depois passe as conclusões pro `/ig-plan`, pra próxima semana ser montada na
evidência do próprio usuário e não em padrões genéricos, e pro `/ig-viral`,
pro swipe file ser filtrado pelas fórmulas que funcionam pra esta conta
especificamente.
