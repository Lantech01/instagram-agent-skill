---
name: ig-carousel
description: >-
  Monta um carrossel de Instagram: a capa que faz a pessoa arrastar pro lado, o
  texto slide por slide e os arquivos 1080x1350 pra subir. Use quando o usuário
  disser "carrossel", "faz um carrossel sobre X", "transforma isso num
  carrossel", "slides", "cards", "post de arrastar pro lado", ou tiver uma ideia
  em formato de lista ou de passo a passo que morreria numa imagem só.
---

# ig-carousel

Carrossel é o formato do grid que mais segura a pessoa olhando, porque arrastar
é uma interação e rolar não é. Ele também ganha uma segunda chance: o Instagram
pode mostrar o carrossel de novo, começando de um slide mais à frente, pra quem
não interagiu da primeira vez. Então o slide dois também tem que parar em pé
sozinho.

O formato premia uma ideia quebrada em passos. Ele castiga uma legenda picada em
pedaços.

## Quando usar no lugar de um Reels

Use carrossel quando a ideia tem **sequência e precisa ser relida**: passos, um
método com partes, um antes e depois, uma lista que vale um print. Use Reels
quando a ideia tem movimento, um rosto, ou um desfecho que precisa ser visto
acontecendo.

Se a ideia é uma afirmação só, não é nenhum dos dois. Passe pro `/ig-reel` e
diga isso.

## Estrutura

De 6 a 10 slides. O teto é 20, e 20 quase sempre é um livro que ninguém termina.
Com menos de 5 o arrastar nem começa.

```
1         CAPA      o gancho. 6 palavras ou menos, num tamanho que dá pra ler
                    no grid, em miniatura. Uma linha de promessa embaixo.
2         RISCO     por que isso importa, numa frase. Esse slide também é uma
                    segunda capa, então não pode ser preparação.
3 a N     UMA IDEIA POR SLIDE. Um título de 3 a 7 palavras, no máximo 25
                    palavras embaixo. Se um slide precisa de parágrafo, são dois.
N+1       RESUMO    tudo numa lista. Esse é o slide do print.
ÚLTIMO    CTA       uma ação. Salvar, comentar uma palavra-chave ou seguir. Uma.
```

## Regras do texto dos slides

- **A capa é 80% do resultado.** Seis palavras. Grande. Nada no resto do
  carrossel salva uma capa que ninguém arrasta. Português gasta mais letra que
  inglês: antes de diminuir a fonte, corte artigo, preposição e "que".
- **Desenhe pro corte do grid.** O grid do perfil corta num retângulo em pé,
  mais alto que largo, e a proporção exata já mudou mais de uma vez. Monte em
  1080x1350 e mantenha o texto da capa bem no meio, longe dos 120 pixels de cada
  borda, e o corte deixa de importar.
- **Numere os slides** (3/8). Mais gente chega ao fim quando consegue ver onde
  ele está.
- **Nenhum slide é um parágrafo.** Se não cabe em 25 palavras, divida.
- **O slide de resumo é o que a pessoa printa e manda.** Compartilhamento é o
  sinal mais forte que dá pra conquistar. Faça esse slide se sustentar sozinho,
  legível sem contexto nenhum.
- **O seu @ em todo slide**, pequeno, no canto de baixo. Print viaja sem você:
  vai pro grupo da família, pro status do WhatsApp, pro story dos outros.
- **Texto alternativo pelo menos na capa.** Leitor de tela lê, e o Instagram
  também.

## Montando os arquivos

O Instagram quer 1080x1350 (4:5), JPEG ou PNG, até 20 itens. Monte como HTML e
imprima cada slide:

```bash
# um <section> por slide, 1080x1350, page-break-after: always
# depois Chrome headless --print-to-pdf, ou qualquer HTML-pra-imagem que você já use
```

Escreva o HTML com `width:1080px; height:1350px`, uma cor de destaque só, e
fonte nunca menor que 32px, porque isso é lido num celular a um terço do tamanho
real. Se o projeto tem uma skill de marca ou um design system, use e não invente
paleta.

Acento é problema seu, não do Instagram. Coloque `<meta charset="utf-8">` no
HTML e, antes de fechar a fonte do título, escreva "AÇÃO, CORAÇÃO, PÃO" nela e
olhe. Fonte de display sem til ou sem cedilha faz o navegador trocar só aquela
letra por outra fonte, e a capa sai com um Ã torto no meio.

## Saída

O texto slide por slide primeiro, numa lista numerada que o usuário lê em dez
segundos e edita antes de qualquer coisa ser renderizada. Depois a **legenda**,
que num carrossel é o Trabalho B do `/ig-caption`: aqui a legenda trabalha,
porque a capa já gastou as seis palavras dela.

Passe os dois pelo `/ig-human`. Monte os arquivos só depois que o usuário
aprovar o texto.

```
CARROSSEL  ·  8 slides

1  CAPA    A CLÁUSULA DE R$ 18 MIL
           Uma linha que hoje vai em todo contrato meu.
2  RISCO   O cliente aprovou o trabalho. Nove dias depois, pediu o dinheiro de volta.
3          O QUE ELA DIZ
           Pagamento na entrega, não na aprovação.
...
7  RESUMO  As quatro linhas, em ordem.
8  CTA     Comenta CONTRATO que eu te mando a cláusula inteira.

Legenda: Trabalho B, gancho na linha 1, um pedido, 3 tags.
```

Nada é enviado. O usuário posta.
