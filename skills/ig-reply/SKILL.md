---
name: ig-reply
description: >-
  Cuida dos comentários nos Reels e posts do próprio usuário - escreve as
  respostas pros que valem resposta, em ordem de quais valem. Use quando o
  usuário colar os comentários, disser "responde esses comentários", "me
  ajuda com os comentários", "comentaram X no meu reels", "como eu respondo
  isso", "apareceu um hater", "perguntaram quanto custa nos comentários", ou
  estiver lidando com uma crítica, um hater ou um cliente em potencial nos
  comentários.
---

# ig-reply

A conversa embaixo do seu próprio post é onde o alcance é decidido. Cada
resposta é mais uma interação no post, as respostas que chegam na primeira
hora fazem a maior parte do trabalho, e no Instagram uma resposta também pode
ser um Reels, que é o movimento mais subutilizado da plataforma.

Mas o valor não é igual entre os comentários, então esta skill separa antes de
escrever.

## Entrada

O usuário cola os comentários, de preferência com o @ de cada um. Print serve.
Não raspe a conversa com ferramenta de navegador.

## Triagem primeiro

Separe cada comentário em um de seis grupos e diga as contagens em voz alta:

| grupo | o que é | o que recebe |
| --- | --- | --- |
| **PALAVRA-CHAVE** | a palavra que você pediu pra comentarem ("comenta EU QUERO") | a coisa prometida, enviada na mão ou pela sua ferramenta aprovada |
| **LEAD** | alguém descrevendo o problema que você resolve, ou perguntando "quanto custa?", "como faço pra comprar?", "atende minha cidade?" | uma resposta de verdade em público, depois uma porta |
| **CONTEÚDO** | traz dado, discorda, estende | a resposta mais longa da conversa |
| **PERGUNTA** | uma pergunta que muita gente tem | essa vira um Reels, não só uma resposta |
| **APOIO** | "🔥", "amei", "salvando", "kkkkk", um amigo marcado | uma curtida, e de 3 a 8 palavras no máximo |
| **RUÍDO** | autopromoção, spam ("seja embaixador da nossa marca, chama na DM"), má-fé, provocação | nada, ou uma linha e tchau |

Escreva nessa ordem e pare quando o valor acabar.

## O movimento que quase todo mundo esquece

Se uma pergunta nos comentários é uma que outras trinta pessoas também têm,
**responda com um Reels**. O Instagram prende o comentário no vídeo novo como
figurinha, quem perguntou recebe notificação, e uma pergunta com demanda real
por trás vira um post com o gancho já escrito pra você. Marque toda PERGUNTA
que se qualifica e passe pro `/ig-reel` como fórmula #16.

## Como responder

- **Responda a pergunta de verdade.** Se perguntaram como, diga como, na
  resposta. Não mande a pessoa pro direct pra ouvir uma resposta que ela podia
  ter ali.
- **"Quanto custa?" ganha preço, não "te chamei no direct".** É a regra de
  cima aplicada ao preço: a resposta no comentário serve pra todo mundo que lê
  a conversa depois, e a resposta na DM serve pra uma pessoa. Se o preço é fixo,
  diga o preço. Se depende do caso, diga de onde ele parte e o que faz ele
  mudar.
- **"Como faço pra comprar?" ganha o caminho em uma linha.** Link na bio,
  qual link, o que clicar. Se a venda é mesmo pelo direct ou pelo WhatsApp,
  diga isso e mande a mensagem de verdade, na hora.
- **Use o nome da pessoa uma vez**, no começo, sem ponto de exclamação.
- **Acompanhe o tamanho.** Um comentário de quatro palavras não ganha resposta
  de quatro linhas. Um "amei 😍" não ganha parágrafo.
- **Pra uma crítica:** reconheça primeiro a parte verdadeira, com as palavras
  da pessoa, depois mantenha sua posição. Nunca apague, nunca fique na
  defensiva, nunca responda duas vezes na mesma conversa.
- **Pra um hater:** nada. Resposta é alcance, e alcance é o que ele veio
  buscar. Isso vale também pra resposta lacradora que a plateia ia aplaudir, e
  pra dar print e expor nos stories, que leva o hater pra um público maior do
  que o que ele tinha. Oculte o comentário se for ofensivo. Os controles de
  comentário do Instagram existem, e usar não é perder.
- **Pra um lead:** responda por completo em público. A porta é uma frase no
  fim, e é uma oferta de ajuda, não uma venda. A resposta pública é o que faz a
  próxima pessoa te chamar no direct.

## Comentários de palavra-chave

Se o post usou um pedido de palavra-chave, esses comentários são o motivo de o
post existir. Cada um é uma pessoa que levantou a mão. Responda cada um,
depois mande o que foi prometido. Se o usuário tem automação configurada pelas
ferramentas do próprio Instagram ou por um parceiro aprovado, diga isso e
deixe rodar; se não, as respostas são manuais, e tudo bem nesse volume. Nunca
mande DM em massa pra quem não comentou.

## Saída

Um bloco, agrupado por grupo, cada resposta pronta pra copiar e já
humanizada:

```
RESPOSTAS  ·  84 comentários  ·  41 PALAVRA-CHAVE, 2 LEAD, 3 CONTEÚDO, 2 PERGUNTA, 34 APOIO, 2 RUÍDO

PALAVRA-CHAVE  (41)  manda a cláusula. Uma linha pra cada, mesmo carinho, nada de copiar e colar.

LEAD
@perfil - "aconteceu exatamente isso com a gente em junho"
> O que resolveu pra gente foi tirar o gatilho do pagamento da aprovação, de
> vez. Se ajudar, te mando o texto da cláusula.

@perfil - "quanto custa a revisão de contrato?"
> Carla, começa em R$ {{seu número}} e o que muda o valor é o tamanho do
> contrato. Se quiser, me manda no direct que tipo de contrato é que eu te digo
> em qual faixa cai.

PERGUNTA -> REELS
@perfil - "e se o cliente se recusar a assinar?"
  34 curtidas nesse comentário. Isso é um Reels, não uma resposta. Fórmula #16.

RUÍDO  (2)  ignorados. Responder dá alcance pra eles.
```

Depois, a trava: nada é postado até o usuário dizer sim. Quem cola as
respostas é ele.
