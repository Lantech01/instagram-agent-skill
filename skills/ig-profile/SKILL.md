---
name: ig-profile
description: >-
  Dá nota de 0 a 100 pra um perfil de Instagram numa rubrica de 12 itens e
  reescreve as partes que perdem ponto: campo de nome, bio, link, destaques, os
  três fixados, grid. Use quando o usuário disser "otimiza meu perfil", "arruma
  minha bio", "o que eu coloco na bio", "dá uma nota pro meu Instagram",
  "analisa meu perfil", "por que ninguém me segue", ou colar o perfil e
  perguntar como ele está.
---

# ig-profile

Quase todo mundo otimiza a coisa errada aqui. O perfil não é uma vitrine que as
pessoas ficam olhando. É uma **tela de decisão**, onde a pessoa chega vinda de
um Reels, e ele tem uns três segundos pra responder uma pergunta: tem mais
disso aqui, e é pra mim?

## Entrada

Peça pro usuário colar ou mandar print de: o campo de nome, o @, a bio, pra
onde o link aponta, os nomes dos destaques, o que está fixado e as nove
primeiras capas do grid. Um print do topo do perfil mais as duas primeiras
linhas do grid basta pra uma primeira passada.

Não entre no Instagram no lugar do usuário.

## Dê a nota

Leia o `rubric.json` desta pasta. Doze itens, 100 pontos, cada um com como é a
nota cheia e como ele costuma falhar. Pontue todos os itens, mostre a tabela, dê
o total. Seja honesto. A maioria dos perfis fica na casa dos 30 e dos 40 na
primeira passada, e nota generosa não serve pra nada.

```
NOTA DO PERFIL  38/100

  campo de nome      2/12   só o nome, nenhuma palavra que alguém busca
  bio, linha um      3/12   três substantivos e um emoji de café
  três fixados       0/10   nada fixado
  destaques          2/8    "Aleatórios", "Vida", "2023"
  grid legível       4/8    seis das nove capas são um rosto no meio da frase
  ...
```

## Depois reescreva, nesta ordem

Corrija em ordem decrescente de pontos perdidos. Não reescreva tudo de uma vez:
o usuário tem que ir lá e mudar cada uma dessas coisas na mão.

**1. O campo de nome (30 caracteres).** A linha em negrito embaixo da foto, não
o @. É o campo que a busca do Instagram compara, e a maioria das contas coloca
um nome nele e mais nada. Formato que funciona:
`{Nome} | {o que você faz, nas palavras que as pessoas buscam}`, tipo
`Bia Nunes | Finanças pra MEI`. Dê três opções. Português é comprido e 30
caracteres acabam rápido: "pra" no lugar de "para", e nada de "Especialista em".

**2. Bio, linha um.** Pra quem é e o que muda. Não é cargo, não é adjetivo, não
é lista de identidades separadas por barra. O resto dos 150 caracteres carrega
uma prova ou uma oferta direta.

**3. Os três fixados.** Três espaços, três trabalhos diferentes: a melhor prova,
a explicação mais clara da oferta, a melhor apresentação da pessoa. É a correção
de maior alavanca do perfil inteiro e leva quatro toques. Um grid sem nada
fixado mostra o que foi postado por último, o que é cara ou coroa.

**4. Destaques.** De quatro a seis, com o nome das perguntas que um comprador
faz: Valores, Resultados, Como funciona, Sobre mim. "Depoimentos" ou
"Feedbacks" fazem o papel de Resultados. Não "Aleatórios". Apague o resto.

**5. O link.** Um destino que bate com o que a bio acabou de prometer. Pode ter
cinco; dois já é um cardápio, e cardápio converte pior que porta. Se a venda
fecha no WhatsApp, o link direto pro WhatsApp, com uma mensagem pronta, é uma
porta.

**6. Capas do grid.** As nove primeiras, em miniatura. Capa de Reels se
escolhe, não fica o primeiro frame que veio. Quatro palavras de texto na capa
deixam o grid legível numa olhada.

## Saída

Tabela de notas, depois as reescritas em blocos prontos pra copiar, na ordem de
correção, cada uma passada pelo `/ig-human`. Dê a nota de novo no fim e mostre a
diferença com honestidade. Se a reescrita chega a 84 e não a 98, diga 84, e diga
do que o resto precisa, que normalmente é um grid, um hábito de stories e um
post fixado que ainda não existe. Nada disso é reescrita.

Nada é salvo no Instagram por esta skill. O usuário edita cada campo.
